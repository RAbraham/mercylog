from abc import ABC, abstractmethod

# import abcdatalog.ast.visitors.PremiseVisitor;
# from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from typing import *

I = TypeVar("I")
O = TypeVar("O")


# /**
#  * A premise in the body of a clause. This interface is under-specified to allow
#  * the addition of new language features.
#  *
#  */


class Premise(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def accept_premise_visitor(self, premise_visitor, state: I) -> O:
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
# import abcdatalog.ast.visitors.PremiseVisitor;
#
# /**
#  * A premise in the body of a clause. This interface is under-specified to allow
#  * the addition of new language features.
#  *
#  */
# public interface Premise {
# 	public <I, O> O accept(PremiseVisitor<I, O> visitor, I state);
# }
