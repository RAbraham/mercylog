from typing import *
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.term_helpers import TermHelpers
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.util.substitution.const_only_substitution import (
    ConstOnlySubstitution,
)

#
# /**
#  * A mapping from variables to constants.
#  *
#  */
class SimpleConstSubstitution(ConstOnlySubstitution):

    # 	/**
    # 	 * The map that represents the substitution.
    # 	 */
    #
    # 	/**
    # 	 * Constructs an empty substitution.
    # 	 */
    # 	/**
    # 	 * Constructs a copy of another substitution.
    # 	 *
    # 	 * @param other
    # 	 *            the other substitution
    # 	 */

    def __init__(self, other: "SimpleConstSubstitution" = None):
        if other:
            self.subst = other.subst
        else:
            self.subst = {}
        super(SimpleConstSubstitution, self).__init__()

    #
    # 	/**
    # 	 * Returns the constant a variable is mapped to in this substitution.
    # 	 *
    # 	 * @param v
    # 	 *            the variable
    # 	 * @return the constant, or null if v is not mapped
    # 	 */
    def get(self, v: Variable) -> Constant:
        return self.subst.get(v)

    #
    # 	/**
    # 	 * Adds a mapping from a variable to a constant to this substitution.
    # 	 *
    # 	 * @param v
    # 	 *            the variable
    # 	 * @param c
    # 	 *            the constant
    # 	 * @throws IllegalArgumentException
    # 	 *             if v is already mapped to another constant
    # 	 */

    def put(self, v: Variable, c: Constant) -> None:
        val: Constant = self.subst.get(v)
        if val and val != c:
            raise ValueError("Cannot remap a variable to another constant.")
        self.subst[v] = c

    # 	/**
    # 	 * Creates a substitution from unifying two lists of terms, the second of
    # 	 * which must be ground (i.e., contain no variables).
    # 	 *
    # 	 * @param xs
    # 	 *            the first list
    # 	 * @param ys
    # 	 *            the second list, which must be ground
    # 	 * @return the substitution, or null if the unification is not possible
    # 	 * @throws IllegalArgumentException
    # 	 *             if the second list of terms is not ground
    # 	 */
    @staticmethod
    def unify(xs: List[Term], ys: List[Term]) -> Optional["SimpleConstSubstitution"]:
        if len(xs) != len(ys):
            return None
        r = SimpleConstSubstitution()
        z = zip(xs, ys)
        for x, y in z:
            if not TermHelpers.unify_const_only_substitution(x, y, r):
                return None

        return r

    def apply(self, terms: List[Term]) -> List[Term]:
        newTerms = []
        for t in terms:
            _t = t
            if isinstance(_t, Variable):
                s: Constant = self.subst.get(_t)
                if s:
                    _t = s
            newTerms.append(_t)
        return newTerms

    def __str__(self):
        elements = [f"{v}->{vv}" for v, vv in self.subst.items()]
        _strs = ",".join(elements)
        result = "[" + _strs + "]"
        return result

    def add(self, x: Variable, c: Constant) -> bool:
        c1: Constant = self.get(x)
        if c1 and c != c1:
            return False
        self.subst[x] = c
        return True

