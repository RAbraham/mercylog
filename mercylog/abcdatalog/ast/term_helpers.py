from typing import *
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
from mercylog.abcdatalog.util.substitution.const_only_substitution import ConstOnlySubstitution
from mercylog.abcdatalog.util.substitution.term_unifier import TermUnifier
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.constant import Constant

T = TypeVar("T")



#
# /**
#  * A utility class for common operations on terms.
#  *
#  */

# public final class TermHelpers {
class TermHelpers:

    @staticmethod
    def  fold(terms: Iterable[Term], tv: TermVisitor[T, T], init: T) -> T:
        acc: T = init
        for t in terms:
            acc = t.accept_term_visitor(tv, acc)
        return acc

# 	public static boolean unify(Term u, Term v, ConstOnlySubstitution s) {
# 		if (u instanceof Variable) {
# 			Constant c = s.get((Variable) u);
# 			if (c != null) {
# 				u = c;
# 			}
# 		}
#
# 		if (v instanceof Variable) {
# 			Constant c = s.get((Variable) v);
# 			if (c != null) {
# 				v = c;
# 			}
# 		}
#
# 		boolean uVar = u instanceof Variable;
# 		boolean vVar = v instanceof Variable;
#
# 		if (uVar && vVar) {
# 			throw new IllegalArgumentException("Cannot unify two variables.");
# 		} else if (uVar) {
# 			assert v instanceof Constant;
# 			s.add((Variable) u, (Constant) v);
# 		} else if (vVar) {
# 			assert u instanceof Constant;
# 			s.add((Variable) v, (Constant) u);
# 		} else {
# 			assert u instanceof Constant && v instanceof Constant;
# 			return u.equals(v);
# 		}
# 		return true;
# 	}
#
    @staticmethod
    def unify_const_only_substitution(u: Term, v: Term, s: ConstOnlySubstitution) -> bool:
        if isinstance(u, Variable):
            c: Constant = s.get(u)
            if c:
                u = c
        if isinstance(v, Variable):
            c: Constant = s.get(v)
            if c:
                v = c
        uVar: bool = isinstance(u, Variable)
        vVar: bool = isinstance(v, Variable)

        if uVar and vVar:
            raise ValueError("Cannot unify two variables.")
        elif uVar:
            assert isinstance(v, Constant)
            s.add(u, v)
        elif vVar:
            assert isinstance(u, Constant)
            s.add(v, u)
        else:
            assert  isinstance(u, Constant) and isinstance(v, Constant)
            return u == v

        return True

        pass

# 	public static boolean unify(Term u, Term v, TermUnifier s) {
# 		if (u instanceof Variable) {
# 			Term t = s.get((Variable) u);
# 			if (t != null) {
# 				u = t;
# 			}
# 		}
#
# 		if (v instanceof Variable) {
# 			Term t = s.get((Variable) v);
# 			if (t != null) {
# 				v = t;
# 			}
# 		}
#
# 		boolean uVar = u instanceof Variable;
# 		boolean vVar = v instanceof Variable;
#
# 		if (uVar) {
# 			return s.unify((Variable) u, v);
# 		} else if (vVar) {
# 			assert u instanceof Constant;
# 			return s.unify((Variable) v, u);
# 		} else {
# 			assert u instanceof Constant && v instanceof Constant;
# 			return u.equals(v);
# 		}
# 	}
# }
    @staticmethod
    def unify_term_unifier(u: Term, v: Term, s: TermUnifier) -> bool:
        if isinstance(u, Variable):
            t: Term = s.get(u)
            if t:
                u = t
        if isinstance(v, Variable):
            t: Term = s.get(v)

            if t:
                v = t
        uVar: bool = isinstance(u, Variable)
        vVar: bool = isinstance(v, Variable)

        if uVar:
            return s.unify(u, v)
        elif vVar:
            assert isinstance(u, Constant)
            return s.unify(v, u)
        else:
            assert isinstance(u, Constant) and isinstance(v, Constant)
            return  u == v

        pass
    pass
# /*******************************************************************************
#  * This file is part of the AbcDatalog project.
#  *
#  * Copyright (c) 2016, Harvard University
#  * All rights reserved.
#  *
#  * This program and the accompanying materials are made available under
#  * the terms of the BSD License which accompanies this distribution.
#  *
#  * The development of the AbcDatalog project has been supported by the
#  * National Science Foundation under Grant Nos. 1237235 and 1054172.
#  *
#  * See README for contributors.
#  ******************************************************************************/
# package abcdatalog.ast;
#
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.util.substitution.ConstOnlySubstitution;
# import abcdatalog.util.substitution.TermUnifier;
#
# /**
#  * A utility class for common operations on terms.
#  *
#  */
# public final class TermHelpers {
# 	private TermHelpers() {
#
# 	}
#
# 	public static <T> T fold(Iterable<Term> terms, TermVisitor<T, T> tv, T init) {
# 		T acc = init;
# 		for (Term t : terms) {
# 			acc = t.accept(tv, acc);
# 		}
# 		return acc;
# 	}
#
# 	public static <T> T fold(Term[] terms, TermVisitor<T, T> tv, T init) {
# 		T acc = init;
# 		for (Term t : terms) {
# 			acc = t.accept(tv, acc);
# 		}
# 		return acc;
# 	}
#
# 	public static boolean unify(Term u, Term v, ConstOnlySubstitution s) {
# 		if (u instanceof Variable) {
# 			Constant c = s.get((Variable) u);
# 			if (c != null) {
# 				u = c;
# 			}
# 		}
#
# 		if (v instanceof Variable) {
# 			Constant c = s.get((Variable) v);
# 			if (c != null) {
# 				v = c;
# 			}
# 		}
#
# 		boolean uVar = u instanceof Variable;
# 		boolean vVar = v instanceof Variable;
#
# 		if (uVar && vVar) {
# 			throw new IllegalArgumentException("Cannot unify two variables.");
# 		} else if (uVar) {
# 			assert v instanceof Constant;
# 			s.add((Variable) u, (Constant) v);
# 		} else if (vVar) {
# 			assert u instanceof Constant;
# 			s.add((Variable) v, (Constant) u);
# 		} else {
# 			assert u instanceof Constant && v instanceof Constant;
# 			return u.equals(v);
# 		}
# 		return true;
# 	}
#
# 	public static boolean unify(Term u, Term v, TermUnifier s) {
# 		if (u instanceof Variable) {
# 			Term t = s.get((Variable) u);
# 			if (t != null) {
# 				u = t;
# 			}
# 		}
#
# 		if (v instanceof Variable) {
# 			Term t = s.get((Variable) v);
# 			if (t != null) {
# 				v = t;
# 			}
# 		}
#
# 		boolean uVar = u instanceof Variable;
# 		boolean vVar = v instanceof Variable;
#
# 		if (uVar) {
# 			return s.unify((Variable) u, v);
# 		} else if (vVar) {
# 			assert u instanceof Constant;
# 			return s.unify((Variable) v, u);
# 		} else {
# 			assert u instanceof Constant && v instanceof Constant;
# 			return u.equals(v);
# 		}
# 	}
# }
