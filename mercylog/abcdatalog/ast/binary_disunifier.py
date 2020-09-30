from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.term import Term
from typing import *
# /**
#  * This premise explicitly disallows the unification of two terms and is represented by the operator {@code !=}. For example, if
#  * {@code X!=a}, then the variable {@code X} cannot be unified with the constant {@code a}.
#  *
#  */

class BinaryDisunifier(Premise):
    def __init__(self, left: Term, right: Term):
        self.left = left
        self.right = right

    def get_left(self) -> Term:
        return self.left

    def get_right(self) -> Term:
        return self.right

    def get_args_iterable(self) -> Sequence:
        return [self.left, self.right]
    pass

    def accept(self, visitor: PremiseVisitor, state):
        return visitor.visit(self, state)

    def __str__(self):
        return self.left + "!= " + self.right

