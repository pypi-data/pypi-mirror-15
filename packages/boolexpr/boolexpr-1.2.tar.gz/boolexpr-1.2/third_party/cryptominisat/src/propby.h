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

#ifndef PROPBY_H
#define PROPBY_H

#include "constants.h"
#include "solvertypes.h"
#include "clause.h"

//#define DEBUG_PROPAGATEFROM

#include "cloffset.h"

namespace CMSat {

enum PropByType {null_clause_t = 0, clause_t = 1, binary_t = 2, tertiary_t = 3, xor_t = 4};

class PropBy
{
    private:
        uint32_t red_step:1;
        uint32_t data1:31;
        uint32_t type:3;
        //0: clause, NULL
        //1: clause, non-null
        //2: binary
        //3: tertiary
        uint32_t data2:29;

    public:
        PropBy() :
            red_step(0)
            , data1(0)
            , type(null_clause_t)
            , data2(0)
        {}

        explicit PropBy(const ClOffset offset) :
            red_step(0)
            , data1(offset)
            , type(clause_t)
            , data2(0)
        {
            //No roll-over
            #ifdef DEBUG_PROPAGATEFROM
            assert(offset == get_offset());
            #endif
        }

        PropBy(const Lit lit, const bool redStep) :
            red_step(redStep)
            , data1(lit.toInt())
            , type(binary_t)
            , data2(0)
        {
        }

        PropBy(size_t xor_num, bool) :
            red_step(0)
            , data1(xor_num)
            , type(xor_t)
            , data2(0)
        {
        }

        //For hyper-bin, etc.
        PropBy(
            const Lit lit
            , bool redStep //Step that lead here from ancestor is redundant
            , bool hyperBin //It's a hyper-binary clause
            , bool hyperBinNotAdded //It's a hyper-binary clause, but was never added because all the rest was zero-level
        ) :
            red_step(redStep)
            , data1(lit.toInt())
            , type(binary_t)
            , data2(0)
        {
            //HACK: if we are doing seamless hyper-bin and transitive reduction
            //then if we are at toplevel, .getAncestor()
            //must work, and return lit_Undef, but at the same time, .isNULL()
            //must also work, for conflict generation. So this is a hack to
            //achieve that. What an awful hack.
            if (lit == ~lit_Undef)
                type = null_clause_t;

            data2 = ((uint32_t)hyperBin) << 1
                | ((uint32_t)hyperBinNotAdded) << 2;
        }

        PropBy(const Lit lit1, const Lit lit2, const bool redStep) :
            red_step(redStep)
            , data1(lit1.toInt())
            , type(tertiary_t)
            , data2(lit2.toInt())
        {
        }

        bool isRedStep() const
        {
            return red_step;
        }

        bool getHyperbin() const
        {
            return data2 & 2U;
        }

        void setHyperbin(bool toSet)
        {
            data2 &= ~2U;
            data2 |= (uint32_t)toSet << 1;
        }

        bool getHyperbinNotAdded() const
        {
            return data2 & 4U;
        }

        void setHyperbinNotAdded(bool toSet)
        {
            data2 &= ~4U;
            data2 |= (uint32_t)toSet << 2;
        }

        Lit getAncestor() const
        {
            #ifdef DEBUG_PROPAGATEFROM
            assert(type == null_clause_t || type == binary_t);
            #endif
            return ~Lit::toLit(data1);
        }

        bool isClause() const
        {
            return type == clause_t;
        }

        bool isXor() const
        {
            return type == xor_t;
        }

        PropByType getType() const
        {
            return (PropByType)type;
        }

        Lit lit2() const
        {
            #ifdef DEBUG_PROPAGATEFROM
            assert(type == tertiary_t || type == binary_t);
            #endif
            return Lit::toLit(data1);
        }

        Lit lit3() const
        {
            #ifdef DEBUG_PROPAGATEFROM
            assert(type == tertiary_t);
            #endif
            return Lit::toLit(data2);
        }

        ClOffset get_offset() const
        {
            #ifdef DEBUG_PROPAGATEFROM
            assert(isClause());
            #endif
            return data1;
        }

        size_t get_xor_num() const
        {
            #ifdef DEBUG_PROPAGATEFROM
            assert(isXor());
            #endif
            return data1;
        }

        bool isNULL() const
        {
            return type == null_clause_t;
        }

        bool operator==(const PropBy other) const
        {
            return (type == other.type
                    && red_step == other.red_step
                    && data1 == other.data1
                    && data2 == other.data2
                   );
        }

        bool operator!=(const PropBy other) const
        {
            return !(*this == other);
        }
};

inline std::ostream& operator<<(std::ostream& os, const PropBy& pb)
{
    switch (pb.getType()) {
        case binary_t :
            os << " binary, other lit= " << pb.lit2();
            break;

        case tertiary_t :
            os << " tri, other 2 lits= " << pb.lit2() << " , "<< pb.lit3();
            break;

        case clause_t :
            os << " clause, num= " << pb.get_offset();
            break;

        case null_clause_t :
            os << " NULL";
            break;

        default:
            assert(false);
            break;
    }
    return os;
}

} //end namespace

#endif //PROPBY_H
