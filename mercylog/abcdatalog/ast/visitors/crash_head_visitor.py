# import abcdatalog.ast.PositiveAtom;
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
#
from mercylog.abcdatalog.ast.visitors.head_visitor import HeadVisitor
from abc import ABC, abstractmethod

from typing import *

I = TypeVar("I")
O = TypeVar("O")


class CrashHeadVisitor(ABC, HeadVisitor):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def visit(self, atom, state: I) -> O:
        pass
# public class CrashHeadVisitor<I, O> implements HeadVisitor<I, O> {
#
# 	@Override
# 	public O visit(PositiveAtom atom, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# }
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
# import abcdatalog.ast.PositiveAtom;
#
# public class CrashHeadVisitor<I, O> implements HeadVisitor<I, O> {
#
# 	@Override
# 	public O visit(PositiveAtom atom, I state) {
# 		throw new UnsupportedOperationException();
# 	}
#
# }
