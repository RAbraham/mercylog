from typing import *
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
from mercylog.abcdatalog.util.substitution.const_only_substitution import (
    ConstOnlySubstitution,
)
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
    def fold(terms: Iterable[Term], tv: TermVisitor[T, T], init: T) -> T:
        acc: T = init
        for t in terms:
            acc = t.accept_term_visitor(tv, acc)
        return acc

    @staticmethod
    def unify_const_only_substitution(
        u: Term, v: Term, s: ConstOnlySubstitution
    ) -> bool:
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
            assert isinstance(u, Constant) and isinstance(v, Constant)
            return u == v

        return True

        pass

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
            return u == v

