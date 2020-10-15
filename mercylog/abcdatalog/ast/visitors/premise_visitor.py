from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
from typing import *
from abc import ABC, abstractmethod

from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.postive_atom import PositiveAtom

# import abcdatalog.engine.bottomup.AnnotatedAtom;
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom

I = TypeVar("I")
O = TypeVar("O")
V = TypeVar("V")


class PremiseVisitor(Generic[I, O], ABC):
    def __init__(self):
        super().__init__()

    # @abstractmethod
    # def visit(self, visited: V, state: I) -> O:
    #     pass

    @abstractmethod
    def visit_positive_atom(self, atom: PositiveAtom, state: I) -> O:
        pass

    @abstractmethod
    def visit_annotated_atom(self, atom: AnnotatedAtom, state: I) -> O:
        pass

    @abstractmethod
    def visit_binary_unifier(self, u: BinaryUnifier, state: I) -> O:
        pass

    @abstractmethod
    def visit_binary_disunifier(self, u: BinaryDisunifier, state: I) -> O:
        pass

    @abstractmethod
    def visit_negated_atom(self, atom: NegatedAtom, state: I) -> O:
        pass




