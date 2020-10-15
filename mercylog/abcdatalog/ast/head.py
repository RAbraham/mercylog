from abc import ABC, abstractmethod
from typing import *
from mercylog.abcdatalog.ast.visitors.head_visitor import HeadVisitor

# /**
#  * The head of a clause. This interface is under-specified to allow the addition
#  * of new language features.
#  *
#  */

I = TypeVar("I")
O = TypeVar("O")



class Head(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def accept_head_visitor(self, visitor: HeadVisitor[I, O], state: I) -> O:
        pass


# *********************************************************************
# import abcdatalog.ast.visitors.HeadVisitor;
#
# /**
#  * The head of a clause. This interface is under-specified to allow the addition
#  * of new language features.
#  *
#  */
# public interface Head {
# 	public <I, O> O accept(HeadVisitor<I, O> visitor, I state);
# }
