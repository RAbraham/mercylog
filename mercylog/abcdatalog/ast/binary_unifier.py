# import abcdatalog.ast.visitors.PremiseVisitor;
# from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.premise import Premise
from typing import *

 # * This premise explicitly unifies two terms and is visually represented as the
 # * operator {@code =}. For example, if {@code X=a}, then the variable {@code X}
 # * is bound to the constant {@code a}.
 # *
 #
class BinaryUnifier(Premise):
    def __init__(self, left: Term, right: Term):
        self.left = left
        self.right = right
        super(BinaryUnifier, self).__init__()

    def getLeft(self) -> Term:
        return self.left

    def getRight(self) -> Term:
        return self.right

    def getArgsIterable(self) -> Sequence:
        return [self.left, self.right]

    def accept(self, visitor, state):
        return visitor.visit_binary_unifier(self, state)

    def __str__(self):
        return str(self.left) + " = " + str(self.right)
