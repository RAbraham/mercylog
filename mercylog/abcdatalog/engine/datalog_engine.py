from abc import ABC, abstractmethod
from typing import *
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom

#
# /**
#  * A Datalog evaluation engine. Datalog engines are initialized with a set of
#  * clauses that represent initial facts and rules that can be used to derive new
#  * facts. After initialization, clients can query about whether certain facts
#  * are derivable.
#  *
#  */
# public interface DatalogEngine {
class DatalogEngine(ABC):

    def __init__(self):
        super().__init__()

    # 	/**
    # 	 * Initializes engine with a Datalog program, including EDB facts. The set
    # 	 * that is passed into this method should include rules for deriving new
    # 	 * facts as well as the initial facts, which can be encoded as clauses with
    # 	 * empty bodies.
    # 	 *
    # 	 * @param program
    # 	 *            program to evaluate
    # 	 * @throws DatalogValidationException
    # 	 * @throws IllegalStateException
    # 	 *             if this engine has already been initialized
    # 	 * @throws DatalogValidationException
    # 	 *             if the given program is invalid
    # 	 */
    # 	void init(Set<Clause> program) throws DatalogValidationException;
    @abstractmethod
    def init(self, program: Set[Clause]):
        pass
#
# 	/**
# 	 * Returns all facts that 1) can be derived from the rules and initial facts
# 	 * that were used to initialize this engine and 2) unify with the query.
# 	 *
# 	 * @param q
# 	 *            the query
# 	 * @return facts
# 	 * @throws IllegalStateException
# 	 *             if this engine has not been initialized with a program
# 	 */
# 	Set<PositiveAtom> query(PositiveAtom q);

    @abstractmethod
    def query(self, q: PositiveAtom) -> Set[PositiveAtom]:
        pass
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
# package abcdatalog.engine;
#
# import java.util.Set;
#
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.validation.DatalogValidationException;
#
# /**
#  * A Datalog evaluation engine. Datalog engines are initialized with a set of
#  * clauses that represent initial facts and rules that can be used to derive new
#  * facts. After initialization, clients can query about whether certain facts
#  * are derivable.
#  *
#  */
# public interface DatalogEngine {
# 	/**
# 	 * Initializes engine with a Datalog program, including EDB facts. The set
# 	 * that is passed into this method should include rules for deriving new
# 	 * facts as well as the initial facts, which can be encoded as clauses with
# 	 * empty bodies.
# 	 *
# 	 * @param program
# 	 *            program to evaluate
# 	 * @throws DatalogValidationException
# 	 * @throws IllegalStateException
# 	 *             if this engine has already been initialized
# 	 * @throws DatalogValidationException
# 	 *             if the given program is invalid
# 	 */
# 	void init(Set<Clause> program) throws DatalogValidationException;
#
# 	/**
# 	 * Returns all facts that 1) can be derived from the rules and initial facts
# 	 * that were used to initialize this engine and 2) unify with the query.
# 	 *
# 	 * @param q
# 	 *            the query
# 	 * @return facts
# 	 * @throws IllegalStateException
# 	 *             if this engine has not been initialized with a program
# 	 */
# 	Set<PositiveAtom> query(PositiveAtom q);
# }
