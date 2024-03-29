from abc import ABC, abstractmethod
from typing import *
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
# from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
#
# /**
#  * A Datalog program for which each rule and initial fact has been independently
#  * validated, but the program as a whole has not been validated. That is, it
#  * guarantees that each clause of a program is independently valid, but says
#  * nothing about whether the clauses taken together make sense. This might be a
#  * concern for language features such as negation, where certain dependencies
#  * between clauses are undesirable.
#  *
#  */

class UnstratifiedProgram(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def getRules(self) -> Set:
        pass

    @abstractmethod
    def getInitialFacts(self) -> Set[PositiveAtom]:
        pass

    @abstractmethod
    def getEdbPredicateSyms(self) -> Set[PredicateSym]:
        pass

    @abstractmethod
    def getIdbPredicateSyms(self) -> Set[PredicateSym]:
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
# package abcdatalog.ast.validation;
#
# import java.util.Set;
#
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.validation.DatalogValidator.ValidClause;
#
# /**
#  * A Datalog program for which each rule and initial fact has been independently
#  * validated, but the program as a whole has not been validated. That is, it
#  * guarantees that each clause of a program is independently valid, but says
#  * nothing about whether the clauses taken together make sense. This might be a
#  * concern for language features such as negation, where certain dependencies
#  * between clauses are undesirable.
#  *
#  */
# public interface UnstratifiedProgram {
# 	Set<ValidClause> getRules();
#
# 	Set<PositiveAtom> getInitialFacts();
#
# 	Set<PredicateSym> getEdbPredicateSyms();
#
# 	Set<PredicateSym> getIdbPredicateSyms();
# }
