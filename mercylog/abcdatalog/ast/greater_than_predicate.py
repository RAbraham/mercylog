from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.premise import Premise
from typing import *


class GreaterThanPredicate(Premise):
    def __init__(self, left: Term, right: Term):
        self.left = left
        self.right = right
        super(GreaterThanPredicate, self).__init__()

    def getLeft(self) -> Term:
        return self.left

    def getRight(self) -> Term:
        return self.right

    def getArgsIterable(self) -> Sequence:
        return [self.left, self.right]

    def accept_premise_visitor(self, premise_visitor, state):
        return premise_visitor.visit_binary_unifier(self, state)

    def __str__(self):
        return str(self.left) + " > " + str(self.right)
