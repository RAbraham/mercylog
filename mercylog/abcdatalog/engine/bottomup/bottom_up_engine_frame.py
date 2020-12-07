from typing import *
# import abcdatalog.ast.Clause;
from mercylog.abcdatalog.ast.clause import Clause
# import abcdatalog.ast.PositiveAtom;
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
# import abcdatalog.ast.validation.DatalogValidationException;
from mercylog.abcdatalog.ast.validation.datalog_validation_exception import DatalogValidationException
# import abcdatalog.engine.DatalogEngine;
from mercylog.abcdatalog.engine.datalog_engine import DatalogEngine
# import abcdatalog.util.datastructures.IndexableFactCollection;
from mercylog.abcdatalog.util.datastructures.indexable_fact_collection import IndexableFactCollection
from mercylog.abcdatalog.engine.bottomup.eval_manager import EvalManager
#
# /**
#  * A framework for a bottom-up Datalog engine.
#  *
#  */
# public class BottomUpEngineFrame implements DatalogEngine {
class BottomUpEngineFrame(DatalogEngine):
# 	/**
# 	 * The evaluation manager for this engine.
# 	 */
# 	private final EvalManager manager;
# 	/**
# 	 * The set of facts that can be derived from the current program.
# 	 */
# 	private volatile IndexableFactCollection facts;
# 	/**
# 	 * Has the engine been initialized?
# 	 */
# 	private volatile boolean isInitialized = false;
#
# 	/**
# 	 * Constructs a bottom-up engine with the provided evaluation manager.
# 	 *
# 	 * @param manager
# 	 *            the manager
# 	 */
# 	public BottomUpEngineFrame(EvalManager manager) {
# 		this.manager = manager;
# 	}
    def __init__(self, manager: EvalManager):
        self.manager = manager
        self.isInitialized = False
        self.facts: Optional[IndexableFactCollection] = None
#
# 	@Override
# 	public synchronized void init(Set<Clause> program) throws DatalogValidationException {
# 		if (this.isInitialized) {
# 			throw new IllegalStateException("Cannot initialize an engine more than once.");
# 		}
#
# 		this.manager.initialize(program);
# 		this.facts = this.manager.eval();
# 		this.isInitialized = true;
# 	}
    def init(self, program: Set[Clause]):
        if self.isInitialized:
            raise ValueError("Cannot initialize an engine more than once.")
        self.manager.initialize(program)
        self.facts = self.manager.eval()
        self.isInitialized = True
#
# 	@Override
# 	public Set<PositiveAtom> query(PositiveAtom q) {
    def query(self, q: PositiveAtom) -> Set[PositiveAtom]:
# 		if (!this.isInitialized) {
# 			throw new IllegalStateException("Engine must be initialized before it can be queried.");
# 		}
        if not self.isInitialized:
            raise ValueError("Engine must be initialized before it can be queried.")

# 		Set<PositiveAtom> r = new HashSet<>();
        r: Set[PositiveAtom] = set()

# 		for (PositiveAtom a : this.facts.indexInto(q)) {
        a: PositiveAtom
        for a in self.facts.indexInto_patom(q):
# 			if (q.unify(a) != null) {
            if q.unify(a) is not None:
# 				r.add(a);
                r.add(a)
# 			}
# 		}
# 		return r;
        return r
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
# package abcdatalog.engine.bottomup;
#
# import java.util.HashSet;
# import java.util.Set;
#
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.validation.DatalogValidationException;
# import abcdatalog.engine.DatalogEngine;
# import abcdatalog.util.datastructures.IndexableFactCollection;
#
# /**
#  * A framework for a bottom-up Datalog engine.
#  *
#  */
# public class BottomUpEngineFrame implements DatalogEngine {
# 	/**
# 	 * The evaluation manager for this engine.
# 	 */
# 	private final EvalManager manager;
# 	/**
# 	 * The set of facts that can be derived from the current program.
# 	 */
# 	private volatile IndexableFactCollection facts;
# 	/**
# 	 * Has the engine been initialized?
# 	 */
# 	private volatile boolean isInitialized = false;
#
# 	/**
# 	 * Constructs a bottom-up engine with the provided evaluation manager.
# 	 *
# 	 * @param manager
# 	 *            the manager
# 	 */
# 	public BottomUpEngineFrame(EvalManager manager) {
# 		this.manager = manager;
# 	}
#
# 	@Override
# 	public synchronized void init(Set<Clause> program) throws DatalogValidationException {
# 		if (this.isInitialized) {
# 			throw new IllegalStateException("Cannot initialize an engine more than once.");
# 		}
#
# 		this.manager.initialize(program);
# 		this.facts = this.manager.eval();
# 		this.isInitialized = true;
# 	}
#
# 	@Override
# 	public Set<PositiveAtom> query(PositiveAtom q) {
# 		if (!this.isInitialized) {
# 			throw new IllegalStateException("Engine must be initialized before it can be queried.");
# 		}
#
# 		Set<PositiveAtom> r = new HashSet<>();
# 		for (PositiveAtom a : this.facts.indexInto(q)) {
# 			if (q.unify(a) != null) {
# 				r.add(a);
# 			}
# 		}
# 		return r;
# 	}
#
# }
