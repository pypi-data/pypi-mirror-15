/*
 * CryptoMiniSat
 *
 * Copyright (c) 2009-2015, Mate Soos. All rights reserved.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation
 * version 2.0 of the License.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301  USA
*/

#include "distiller.h"
#include "clausecleaner.h"
#include "time_mem.h"
#include "solver.h"
#include "watchalgos.h"
#include "clauseallocator.h"
#include "sqlstats.h"

#include <iomanip>
using namespace CMSat;
using std::cout;
using std::endl;

//#define DEBUG_STAMPING

#ifdef VERBOSE_DEBUG
#define VERBOSE_SUBSUME_NONEXIST
#endif

//#define VERBOSE_SUBSUME_NONEXIST

Distiller::Distiller(Solver* _solver) :
    solver(_solver)
{}

bool Distiller::distill(const bool alsoStrengthen)
{
    assert(solver->ok);
    numCalls++;

    solver->clauseCleaner->clean_clauses(solver->longIrredCls);

    if (alsoStrengthen
        && !distill_long_irred_cls()
    ) {
        goto end;
    }

    if (alsoStrengthen
        && !distill_tri_irred_cls()
    ) {
        goto end;
    }

end:
    globalStats += runStats;
    if (solver->conf.verbosity >= 1) {
        if (solver->conf.verbosity >= 3)
            runStats.print(solver->nVars());
        else
            runStats.print_short(solver);
    }
    runStats.clear();

    return solver->ok;
}

bool Distiller::distill_tri_irred_cls()
{
    if (solver->conf.verbosity >= 6) {
        cout
        << "c Doing distill for tri irred clauses"
        << endl;
    }

    //solver->watches.size()-1 would overflow
    if (solver->watches.size() == 0) {
        return solver->ok;
    }

    uint64_t origShorten = runStats.numClShorten;
    uint64_t origLitRem = runStats.numLitsRem;
    const double myTime = cpuTime();
    uint64_t maxNumProps =
        2LL*1000LL*solver->conf.distill_time_limitM
        *solver->conf.global_timeout_multiplier;
    uint64_t oldBogoProps = solver->propStats.bogoProps;
    size_t origTrailSize = solver->trail_size();

    //Randomize start in the watchlist
    size_t upI;
    upI = solver->mtrand.randInt(solver->watches.size()-1);
    size_t numDone = 0;
    for (; numDone < solver->watches.size()
        ; upI = (upI +1) % solver->watches.size(), numDone++

    ) {
        if (solver->propStats.bogoProps-oldBogoProps + extraTime > maxNumProps
            || solver->must_interrupt_asap()
        ) {
            break;
        }

        Lit lit = Lit::toLit(upI);
        for (size_t i = 0; i < solver->watches[upI].size(); i++) {
            if (solver->propStats.bogoProps-oldBogoProps + extraTime > maxNumProps) {
                break;
            }

            Watched ws = solver->watches[upI][i];

            //Only irred TRI and each TRI only once
            if (ws.isTri()
                && !ws.red()
                && lit < ws.lit2()
                && ws.lit2() < ws.lit3()
            ) {
                uselessLits.clear();
                lits.resize(3);
                lits[0] = lit;
                lits[1] = ws.lit2();
                lits[2] = ws.lit3();
                try_distill_clause_and_return_new(
                    CL_OFFSET_MAX
                    , ws.red()
                    , 2
                );

                //We could have modified the watchlist, better exit now
                break;
            }
        }

        if (!solver->okay()) {
            break;
        }
    }

    int64_t diff_bogoprops = (int64_t)solver->propStats.bogoProps-(int64_t)oldBogoProps;
    const bool time_out =  diff_bogoprops + extraTime > maxNumProps;
    const double time_used = cpuTime() - myTime;
    const double time_remain = 1.0 - calc_percentage(diff_bogoprops + extraTime, maxNumProps);
    if (solver->conf.verbosity >= 3) {
        cout
        << "c [distill] tri irred"
        << " shorten: " << runStats.numClShorten - origShorten
        << " lit-rem: " << runStats.numLitsRem - origLitRem
        << " 0-depth ass: " << solver->trail_size() - origTrailSize
        << solver->conf.print_times(time_used, time_out, time_remain)
        << endl;
    }
    if (solver->sqlStats) {
        solver->sqlStats->time_passed(
            solver
            , "distill tri irred"
            , time_used
            , time_out
            , time_remain
        );
    }

    runStats.zeroDepthAssigns = solver->trail_size() - origTrailSize;

    return solver->ok;
}

struct ClauseSizeSorter
{
    ClauseSizeSorter(const ClauseAllocator& _cl_alloc, const bool _invert = false) :
        cl_alloc(_cl_alloc)
        , invert(_invert)
    {}

    const ClauseAllocator& cl_alloc;
    const bool invert;

    bool operator()(const ClOffset off1, const ClOffset off2) const
    {
        const Clause* cl1 = cl_alloc.ptr(off1);
        const Clause* cl2 = cl_alloc.ptr(off2);

        if (!invert)
            return cl1->size() > cl2->size();
        else
            return cl1->size() < cl2->size();
    }
};

bool Distiller::distill_long_irred_cls()
{
    assert(solver->ok);
    if (solver->conf.verbosity >= 6) {
        cout
        << "c Doing distillation branch for long irred clauses"
        << endl;
    }

    double myTime = cpuTime();
    const size_t origTrailSize = solver->trail_size();

    //Time-limiting
    uint64_t maxNumProps =
        solver->conf.distill_long_irred_cls_time_limitM*1000LL*1000ULL
        *solver->conf.global_timeout_multiplier;
    if (solver->litStats.irredLits + solver->litStats.redLits < 500000)
        maxNumProps *=2;

    extraTime = 0;
    uint64_t oldBogoProps = solver->propStats.bogoProps;
    bool time_out = false;
    runStats.potentialClauses = solver->longIrredCls.size();
    runStats.numCalled = 1;

    std::sort(solver->longIrredCls.begin(), solver->longIrredCls.end(), ClauseSizeSorter(solver->cl_alloc));
    uint64_t origLitRem = runStats.numLitsRem;
    uint64_t origClShorten = runStats.numClShorten;

    uint32_t queueByBy = 2;
    if (numCalls > 8
        && (solver->litStats.irredLits + solver->litStats.redLits < 4000000)
        && (solver->longIrredCls.size() < 50000)
    ) {
        queueByBy = 1;
    }

    vector<ClOffset>::iterator i, j;
    i = j = solver->longIrredCls.begin();
    for (vector<ClOffset>::iterator end = solver->longIrredCls.end()
        ; i != end
        ; i++
    ) {
        //Check if we are in state where we only copy offsets around
        if (time_out || !solver->ok) {
            *j++ = *i;
            continue;
        }

        //if done enough, stop doing it
        if (solver->propStats.bogoProps-oldBogoProps + extraTime >= maxNumProps
            || solver->must_interrupt_asap()
        ) {
            if (solver->conf.verbosity >= 3) {
                cout
                << "c Need to finish distillation -- ran out of prop (=allocated time)"
                << endl;
            }
            runStats.timeOut++;
            time_out = true;
        }

        //Get pointer
        ClOffset offset = *i;
        Clause& cl = *solver->cl_alloc.ptr(offset);
        //Time to dereference
        extraTime += 5;

        //If we already tried this clause, then move to next
        if (cl.getdistilled()) {
            *j++ = *i;
            continue;
        } else {
            //Otherwise, this clause has been tried for sure
            cl.set_distilled(true);
        }

        extraTime += cl.size();
        runStats.checkedClauses++;

        //Sanity check
        assert(cl.size() > 3);
        assert(!cl.red());

        //Copy literals
        uselessLits.clear();
        lits.resize(cl.size());
        std::copy(cl.begin(), cl.end(), lits.begin());

        //Try to distill clause
        ClOffset offset2 = try_distill_clause_and_return_new(
            offset
            , cl.red()
            , queueByBy
        );

        if (offset2 != CL_OFFSET_MAX) {
            *j++ = offset2;
        }
    }
    solver->longIrredCls.resize(solver->longIrredCls.size()- (i-j));

    //Didn't time out, so it went through the whole list. Reset distill for all.
    if (!time_out) {
        for (vector<ClOffset>::const_iterator
            it = solver->longIrredCls.begin(), end = solver->longIrredCls.end()
            ; it != end
            ; ++it
        ) {
            Clause* cl = solver->cl_alloc.ptr(*it);
            cl->set_distilled(false);
        }
    }

    const double time_used = cpuTime() - myTime;
    const double time_remain = calc_percentage(solver->propStats.bogoProps-oldBogoProps + extraTime, maxNumProps);
    if (solver->conf.verbosity >= 2) {
        cout << "c [distill] longirred"
        << " tried: " << runStats.checkedClauses << "/" << solver->longIrredCls.size()
        << " cl-r:" << runStats.numClShorten- origClShorten
        << " lit-r:" << runStats.numLitsRem - origLitRem
        << solver->conf.print_times(time_used, time_out, time_remain)
        << endl;
    }
    if (solver->sqlStats) {
        solver->sqlStats->time_passed(
            solver
            , "distill long irred"
            , time_used
            , time_out
            , time_remain
        );
    }

    //Update stats
    runStats.time_used = cpuTime() - myTime;
    runStats.zeroDepthAssigns = solver->trail_size() - origTrailSize;

    return solver->ok;
}

ClOffset Distiller::try_distill_clause_and_return_new(
    ClOffset offset
    , const bool red
    , const uint32_t queueByBy
) {
    #ifdef DRUP_DEBUG
    if (solver->conf.verbosity >= 6) {
        cout
        << "Trying to distill clause:";
        for(size_t i = 0; i < lits.size(); i++) {
            cout << lits[i] << " ";
        }
        cout << endl;
    }
    #endif

    //Try to enqueue the literals in 'queueByBy' amounts and see if we fail
    bool failed = false;
    uint32_t done = 0;
    solver->new_decision_level();
    for (; done < lits.size();) {
        uint32_t i2 = 0;
        for (; (i2 < queueByBy) && ((done+i2) < lits.size()); i2++) {
            lbool val = solver->value(lits[done+i2]);
            if (val == l_Undef) {
                solver->enqueue(~lits[done+i2]);
            } else if (val == l_False) {
                //Record that there is no use for this literal
                uselessLits.push_back(lits[done+i2]);
            }
        }
        done += i2;
        extraTime += 5;
        failed = (!solver->propagate<true>().isNULL());
        if (failed) {
            break;
        }
    }
    solver->cancelUntil<false>(0);
    assert(solver->ok);

    if (uselessLits.size() > 0 || (failed && done < lits.size())) {
        //Stats
        runStats.numClShorten++;
        extraTime += 20;
        const uint32_t origSize = lits.size();

        //Remove useless literals from 'lits'
        lits.resize(done);
        for (uint32_t i2 = 0; i2 < uselessLits.size(); i2++) {
            remove(lits, uselessLits[i2]);
        }

        //Make new clause
        Clause *cl2 = solver->add_clause_int(lits, red);

        //Print results
        if (solver->conf.verbosity >= 5) {
            cout
            << "c Distillation branch effective." << endl;
            if (offset != CL_OFFSET_MAX) {
                cout
                << "c --> orig clause:" <<
                 *solver->cl_alloc.ptr(offset)
                 << endl;
            } else {
                cout
                << "c --> orig clause: TRI/BIN" << endl;
            }
            cout
            << "c --> orig size:" << origSize << endl
            << "c --> new size:" << (cl2 == NULL ? 0 : cl2->size()) << endl
            << "c --> removing lits from end:" << origSize - done << endl
            << "c --> useless lits in middle:" << uselessLits.size()
            << endl;
        }

        //Detach and free old clause
        if (offset != CL_OFFSET_MAX) {
            solver->detachClause(offset);
            solver->cl_alloc.clauseFree(offset);
        }

        runStats.numLitsRem += origSize - lits.size();

        if (cl2 != NULL) {
            cl2->set_distilled(true);

            return solver->cl_alloc.get_offset(cl2);
        } else {
            return CL_OFFSET_MAX;
        }
    } else {
        return offset;
    }
}

Distiller::Stats& Distiller::Stats::operator+=(const Stats& other)
{
    time_used += other.time_used;
    timeOut += other.timeOut;
    zeroDepthAssigns += other.zeroDepthAssigns;
    numClShorten += other.numClShorten;
    numLitsRem += other.numLitsRem;
    checkedClauses += other.checkedClauses;
    potentialClauses += other.potentialClauses;
    numCalled += other.numCalled;

    return *this;
}

void Distiller::Stats::print_short(const Solver* solver) const
{
    cout
    << "c [distill] tri+long"
    << " useful: "<< numClShorten
    << "/" << checkedClauses << "/" << potentialClauses
    << " lits-rem: " << numLitsRem
    << " 0-depth-assigns: " << zeroDepthAssigns
    << solver->conf.print_times(time_used, timeOut)
    << endl;
}

void Distiller::Stats::print(const size_t nVars) const
{
    cout << "c -------- DISTILL STATS --------" << endl;
    print_stats_line("c time"
        , time_used
        , ratio_for_stat(time_used, numCalled)
        , "per call"
    );

    print_stats_line("c timed out"
        , timeOut
        , stats_line_percent(timeOut, numCalled)
        , "% of calls"
    );

    print_stats_line("c distill/checked/potential"
        , numClShorten
        , checkedClauses
        , potentialClauses
    );

    print_stats_line("c lits-rem",
        numLitsRem
    );
    print_stats_line("c 0-depth-assigns",
        zeroDepthAssigns
        , stats_line_percent(zeroDepthAssigns, nVars)
        , "% of vars"
    );
    cout << "c -------- DISTILL STATS END --------" << endl;
}
