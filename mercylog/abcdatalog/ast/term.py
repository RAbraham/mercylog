from abc import ABC, abstractmethod
from typing import *
from mercylog.abcdatalog.ast.visitors.term_visitor import TermVisitor
from mercylog.abcdatalog.util.substitution.substitution import Substitution
#
# /**
#  * A Datalog term (i.e., a constant or variable).
#  *
#  */

I = TypeVar("I")
O = TypeVar("O")


class Term(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def accept_term_visitor(self, visitor: TermVisitor[I, O], state: I):
        pass

    @abstractmethod
    def applySubst(self, subst: Substitution) -> "Term":
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
# package abcdatalog.ast;
#
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.util.substitution.Substitution;
#
# /**
#  * A Datalog term (i.e., a constant or variable).
#  *
#  */
# public interface Term {
# 	public <I, O> O accept(TermVisitor<I, O> visitor, I state);
#
# 	public Term applySubst(Substitution subst);
# }
