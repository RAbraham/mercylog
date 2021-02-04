from typing import *

from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor

#
from typing import *

I = TypeVar("I")
O = TypeVar("O")


class Visitor(TermVisitor[I, O]):
    def __init__(
        self,
        onVariable: Callable[[Variable, I], O],
        onConstant: Callable[[Constant, I], O],
        otherwise: Callable[[Term, I], O],
    ):
        self.onVariable = onVariable
        self.onConstant = onConstant
        self.otherwise = otherwise
        super(Visitor, self).__init__()

    def visit_variable(self, t: Variable, state: I) -> O:
        if self.onVariable:
            return self.onVariable(t, state)
        return self.otherwise(t, state)

    def visit_constant(self, t: Constant, state: I) -> O:
        if self.onConstant:
            return self.onConstant(t, state)
        return self.otherwise(t, state)

    pass


class TermVisitorBuilder(Generic[I, O]):
    def __init__(self):
        self._onVariable = None
        self._onConstant = None

    def onVariable(self, f: Callable[[Variable, I], O]) -> "TermVisitorBuilder[I, O]":
        self._onVariable = f
        return self

    def onConstant(self, f: Callable[[Constant, I], O]) -> "TermVisitorBuilder[I, O]":
        self._onConstant = f
        return self

    def or_(self, f: Callable[[Term, I], O]) -> TermVisitor[I, O]:
        return Visitor(self._onVariable, self._onConstant, f)

    def orNull(self) -> TermVisitor[I, O]:
        return self.or_(lambda t, state: None)

    def orCrash(self) -> TermVisitor[I, O]:
        def raise_error():
            raise NotImplementedError()

        return self.or_(lambda t, state: raise_error())
