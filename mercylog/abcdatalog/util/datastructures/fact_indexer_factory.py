from typing import *
# import abcdatalog.ast.PositiveAtom;
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
# import abcdatalog.util.Utilities;
from mercylog.abcdatalog.util.utilities import Utilities
from mercylog.abcdatalog.util.datastructures.concurrent_fact_indexer import ConcurrentFactIndexer
from queue import Queue
#
# /**
#  * A factory for creating some useful fact indexers.
#  *
#  */
# public final class FactIndexerFactory {
class FactIndexerFactory:
#
# 	private FactIndexerFactory() {
#
# 	}
#
# 	/**
# 	 * Creates a fact indexer that uses concurrent sets for the base container.
# 	 *
# 	 * @return the fact indexer
# 	 */
# 	public static ConcurrentFactIndexer<Set<PositiveAtom>> createConcurrentSetFactIndexer() {
    @staticmethod
    def createConcurrentSetFactIndexer() -> ConcurrentFactIndexer[Set[PositiveAtom]]:
# 		return new ConcurrentFactIndexer<>(() -> Utilities.createConcurrentSet(), (set,
# 				fact) -> set.add(fact));
        generator = lambda: Utilities.createConcurrentSet()
        addFunc = lambda a_set, fact: a_set.add(fact)
        return ConcurrentFactIndexer.create_no_empty(generator, addFunc)
# 	}
#
# 	/**
# 	 * Creates a fact indexer that uses concurrent queues for the base
# 	 * container.
# 	 *
# 	 * @return the fact indexer
# 	 */
# 	public static ConcurrentFactIndexer<Queue<PositiveAtom>> createConcurrentQueueFactIndexer() {
    @staticmethod
    def createConcurrentQueueFactIndexer() -> ConcurrentFactIndexer[Queue[PositiveAtom]]:
        generator = lambda: aaaa
# 		return new ConcurrentFactIndexer<>(() -> new ConcurrentLinkedQueue<>(), (queue,
        return ConcurrentFactIndexer.create_no_empty(generator, addFunc)
# 				fact) -> queue.add(fact));
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
# package abcdatalog.util.datastructures;
#
# import java.util.Queue;
# import java.util.Set;
# import java.util.concurrent.ConcurrentLinkedQueue;
#
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.util.Utilities;
#
# /**
#  * A factory for creating some useful fact indexers.
#  *
#  */
# public final class FactIndexerFactory {
#
# 	private FactIndexerFactory() {
#
# 	}
#
# 	/**
# 	 * Creates a fact indexer that uses concurrent sets for the base container.
# 	 *
# 	 * @return the fact indexer
# 	 */
# 	public static ConcurrentFactIndexer<Set<PositiveAtom>> createConcurrentSetFactIndexer() {
# 		return new ConcurrentFactIndexer<>(() -> Utilities.createConcurrentSet(), (set,
# 				fact) -> set.add(fact));
# 	}
#
# 	/**
# 	 * Creates a fact indexer that uses concurrent queues for the base
# 	 * container.
# 	 *
# 	 * @return the fact indexer
# 	 */
# 	public static ConcurrentFactIndexer<Queue<PositiveAtom>> createConcurrentQueueFactIndexer() {
# 		return new ConcurrentFactIndexer<>(() -> new ConcurrentLinkedQueue<>(), (queue,
# 				fact) -> queue.add(fact));
# 	}
#
# }
