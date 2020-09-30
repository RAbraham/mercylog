from mercylog.abcdatalog.ast.postive_atom import PositiveAtom
from abc import ABC, abstractmethod
from typing import *


I = TypeVar("I")
O = TypeVar("O")


class HeadVisitor(Generic[I, O]):
    @abstractmethod
    def visit(self, atom: PositiveAtom, state: I) -> O:
        pass


# public interface HeadVisitor<I, O> {
# 	public O visit(PositiveAtom atom, I state);
# }
