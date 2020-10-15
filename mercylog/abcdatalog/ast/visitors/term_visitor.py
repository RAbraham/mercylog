from typing import *
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.variable import Variable

I = TypeVar("I")
O = TypeVar("O")

from abc import ABC, abstractmethod


class TermVisitor(ABC, Generic[I, O]):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def visit_variable(self, t: Variable, state: I) -> O:
        pass

    @abstractmethod
    def visit_constant(self, t: Constant, state: I) -> O:
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
# package abcdatalog.ast.visitors;
#
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.Variable;
#
# public interface TermVisitor<I, O> {
# 	public O visit(Variable t, I state);
#
# 	public O visit(Constant t, I state);
# }
