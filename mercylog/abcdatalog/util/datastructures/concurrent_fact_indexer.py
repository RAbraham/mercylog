from typing import *
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.visitors.term_visitor_builder import TermVisitorBuilder
from mercylog.abcdatalog.util.substitution.const_only_substitution import ConstOnlySubstitution
from mercylog.abcdatalog.util.datastructures.fact_indexer import FactIndexer

from mercylog.abcdatalog.util.datastructures.indexable_fact_collection import IndexableFactCollection
T = TypeVar("T")

def make_tv():
# private static final TermVisitor<ConstOnlySubstitution, Constant> tv = (new TermVisitorBuilder<ConstOnlySubstitution, Constant>())
#         .onConstant((c, s) -> c).onVariable((x, s) -> {
#             if (s != null) {
#                 return s.get(x);
#             }
#             return null;
#         }).orCrash();
    def variable_func(x, s):
        if s is not None:
            return s.get(x)
        return None
    tv = TermVisitorBuilder().onConstant(lambda c, s: c).onVariable(variable_func).orCrash()
    return tv

#
# /**
#  * An index that holds facts. The facts are indexed by predicate symbol and then
#  * by the constants in each argument position. The indexer is parameterized by
#  * the type of the container that ultimately holds the facts (i.e., all facts
#  * that belong to the same index are added to the same container).
#  *
#  * In the presence of multiple threads, the indexer can momentarily be in an
#  * inconsistent state. However, after the add method returns having been invoked
#  * with a fact f, the indexer will be consistent with respect to f, meaning that
#  * f is properly indexed and that it is visible as such to all threads. (This
#  * only holds, of course, if the provided container type is thread safe.)
#  *
#  * @param <T>
#  *            the container type
#  */
# public class ConcurrentFactIndexer<T extends Iterable<PositiveAtom>> implements FactIndexer {
# TODO: Currently Python does not have threads, so we'll keep this single threaded for now, later maybe we'll look at concurrency
class ConcurrentFactIndexer(FactIndexer):
# 	private static final TermVisitor<ConstOnlySubstitution, Constant> tv = (new TermVisitorBuilder<ConstOnlySubstitution, Constant>())
# 			.onConstant((c, s) -> c).onVariable((x, s) -> {
# 				if (s != null) {
# 					return s.get(x);
# 				}
# 				return null;
# 			}).orCrash();
#
    tv = make_tv()

# 	private final Supplier<T> generator;
# 	private final BiConsumer<T,PositiveAtom> addFunc;
# 	private final Supplier<T> empty;
#
# 	private final ConcurrentMap<PredicateSym, AtomicReferenceArray<ConcurrentMap<Constant, T>>> fineIdx = Utilities.createConcurrentMap();
# 	private final ConcurrentMap<PredicateSym, T> coarseIdx = Utilities.createConcurrentMap();
#

#
# 	/**
# 	 * Creates a new fact indexer.
# 	 *
# 	 * @param generator
# 	 *            an anonymous function that returns a container
# 	 * @param addFunc
# 	 *            an anonymous function that adds a fact to a container
# 	 * @param empty
# 	 *            an anonymous function that returns an empty container (such as
# 	 *            a static instance)
# 	 */
# 	public ConcurrentFactIndexer(Supplier<T> generator, BiConsumer<T,PositiveAtom> addFunc, Supplier<T> empty) {
# 		this.generator = generator;
# 		this.addFunc = addFunc;
# 		this.empty = empty;
# 	}
#
    def __init__(self, generator: Callable[[], T], addFunc: Callable[[T, PositiveAtom], None], empty: Callable[[], T]):
        self.generator = generator
        self.addFunc = addFunc
        self.empty = empty
        self.coarseIdx: Dict[PredicateSym, T] = dict()
        self.fineIdx: Dict[PredicateSym, List[Optional[Dict[Constant, T]]]] = dict()
        super(ConcurrentFactIndexer, self).__init__()

# 	/**
# 	 * Creates a new fact indexer.
# 	 *
# 	 * @param generator
# 	 *            an anonymous function that returns a container
# 	 * @param addFunc
# 	 *            an anonymous function that adds a fact to a container
# 	 */
# 	public ConcurrentFactIndexer(Supplier<T> generator, BiConsumer<T,PositiveAtom> addFunc) {
# 		this(generator, addFunc, generator);
# 	}
    @staticmethod
    def create_no_empty(generator, addFunc):
        return ConcurrentFactIndexer(generator, addFunc, generator)

# 	/**
# 	 * Adds a fact to this indexer.
# 	 *
# 	 * @param fact
# 	 *            the fact
# 	 */
# 	public void add(PositiveAtom fact) {
    def add(self, fact: PositiveAtom):
# 		assert fact.isGround();
        assert fact.isGround()
# 		T rough = this.coarseIdx.get(fact.getPred());
        rough = self.coarseIdx.get(fact.getPred())
# 		if (rough == null) {
        if rough is None:
# 			rough = this.generator.get();
            rough = self.generator()
# 			T existing = this.coarseIdx.putIfAbsent(fact.getPred(), rough);
# 			if (existing != null) {
# 				rough = existing;
# 			}
            existing = self.coarseIdx.get(fact.getPred())
            if existing is None:
                self.coarseIdx[fact.getPred()] = rough
            else:
                rough = existing
# 		}
# 		this.addFunc.accept(rough, fact);
        self.addFunc(rough, fact)
#
# 		AtomicReferenceArray<ConcurrentMap<Constant, T>> byPos = this.fineIdx.get(fact.getPred());
        byPos: List[Optional[Dict[Constant, T]]]
        byPos = self.fineIdx.get(fact.getPred())
# 		if (byPos == null) {
        if byPos is None:
# 			byPos = new AtomicReferenceArray<>(fact.getPred().getArity());
            byPos = fact.getPred().getArity() * [None]
# 			AtomicReferenceArray<ConcurrentMap<Constant, T>> existing = this.fineIdx.putIfAbsent(fact.getPred(), byPos);
# 			if (existing != null) {
# 				byPos = existing;
# 			}
            existing = self.fineIdx.get(fact.getPred())
            if existing is None:
                self.fineIdx[fact.getPred()] = byPos
            else:
                byPos = existing

# 		}
# 		assert byPos != null;
        assert byPos is not None
#
# 		Term[] args = fact.getArgs();
        args = fact.getArgs()
# 		for (int i = 0; i < args.length; ++i) {
        for i, a in enumerate(args):
# 			ConcurrentMap<Constant, T> byConstant = byPos.get(i);
            byConstant = byPos[i]
# 			if (byConstant == null) {
            if byConstant is None:
# 				byConstant = Utilities.createConcurrentMap();
                byConstant = dict()
# 				if (!byPos.compareAndSet(i, null, byConstant)) {
# 					byConstant = byPos.get(i);
# 				}
                a_val = byPos[i]
                if a_val is None:
                    byPos[i] = byConstant
                else:
                    byConstant = byPos[i]
# 			}
# 			Constant key = (Constant) args[i];
            key = args[i]
# 			T n = byConstant.get(key);
            n = byConstant.get(key)
# 			if (n == null) {
            if n is None:
# 				n = this.generator.get();
                n = self.generator()
# 				T existing = byConstant.putIfAbsent(key, n);
# 				if (existing != null) {
# 					n = existing;
# 				}
                existing = byConstant.get(key)
                if existing is None:
                    byConstant[key] = n
                else:
                    n = existing
# 			}
# 			this.addFunc.accept(n, fact);
            self.addFunc(n, fact)
# 		}
# 	}
#
# 	/**
# 	 * Adds the facts to the index.
# 	 *
# 	 * @param facts
# 	 *            the facts
# 	 */
# 	public void addAll(Iterable<PositiveAtom> facts) {
    def addAll_facts(self, facts: Iterable[PositiveAtom]):
# 		for (PositiveAtom a : facts) {
        for a in facts:
# 			this.add(a);
            self.add(a)
# 		}
# 	}
#
# 	@Override
# 	public T indexInto(PositiveAtom a) {
    def indexInto_patom(self, a: PositiveAtom) ->  T:
# 		return this.indexInto(a, null);
        return self.indexInto_patom_with_substitution(a, None)
# 	}
#

# 	@Override
# 	public T indexInto(PositiveAtom a, ConstOnlySubstitution s) {
    def indexInto_patom_with_substitution(self, a: PositiveAtom, s: ConstOnlySubstitution) -> T:
# 		AtomicReferenceArray<ConcurrentMap<Constant, T>> byPos = this.fineIdx.get(a.getPred());
        byPos = self.fineIdx.get(a.getPred())
# 		if (byPos == null) {
# 			return this.empty.get();
# 		}
        if byPos is None:
            return self.empty()
#
# 		int bestIdx = -1;
        bestIdx: int = -1
# 		Term bestConst = null;
        bestConst: Optional[Term] = None
# 		int maxKeySetSize = -1;
        maxKeySetSize: int = -1
# 		Term[] args = a.getArgs();
        args = a.getArgs()
# 		for (int i = 0; i < args.length; ++i) {
        for i, _ in enumerate(args):
# 			Term t = args[i];
            t: Term = args[i]
# //			if (!(t instanceof DummyTerm) && (t instanceof Constant || (s != null && (t = s.get((Variable) t)) != null))) {
# 			if ((t = t.accept(tv, s)) != null) {
            t = t.accept_term_visitor(ConcurrentFactIndexer.tv, s)
            if t is not None:
# 				ConcurrentMap<Constant, T> byConstant = byPos.get(i);
                byConstant: Dict[Constant, T] = byPos[i]
# 				if (byConstant != null) {
                if byConstant is not None:
# 					if (!byConstant.containsKey(t)) {
                    if t not in byConstant:
# 						return this.empty.get();
                        return self.empty()
# 					}
# 					int keySetSize = byConstant.size();
                    keySetSize = len(byConstant)
# 					if (keySetSize > maxKeySetSize) {
                    if keySetSize > maxKeySetSize:
# 						maxKeySetSize = keySetSize;
                        maxKeySetSize = keySetSize
# 						bestIdx = i;
                        bestIdx = i
# 						bestConst = t;
                        bestConst = t
# 					}
# 				}
# 			}
# 		}
#
# 		if (bestIdx == -1) {
# 			return this.coarseIdx.get(a.getPred());
# 		}
        if bestIdx == -1:
            return self.coarseIdx.get(a.getPred())
#
# 		return byPos.get(bestIdx).get(bestConst);
        return byPos[bestIdx].get(bestConst)
# 	}
#
# 	@Override
# 	public T indexInto(PredicateSym pred) {
    def indexInto_predsym(self, pred: PredicateSym):
# 		T t = this.coarseIdx.get(pred);
        t = self.coarseIdx.get(pred)
# 		if (t == null) {
        if t is None:
# 			t = this.empty.get();
            t = self.empty()
# 		}
# 		return t;
        return t
# 	}
#
# 	/**
# 	 * Clears this index.
# 	 */
# 	public void clear() {
    def clear(self):
# 		this.fineIdx.clear();
        self.fineIdx.clear()
# 		this.coarseIdx.clear();
        self.coarseIdx.clear()
# 	}
#
# 	@Override
# 	public boolean isEmpty() {
    def isEmpty(self):
# 		return this.coarseIdx.isEmpty();
        return len(self.coarseIdx) == 0
# 	}
#
# 	public ConcurrentFactIndexer<T> getCopy() {
    def getCopy(self) -> "ConcurrentFactIndexer":
# 		// Lazy man's copy function... probably be faster if we actually
# 		// recursed through data structure copying whole indices. On the other
# 		// hand, that might end up creating a new fact indexer with an
# 		// inconsistent state.
# 		ConcurrentFactIndexer<T> r = new ConcurrentFactIndexer<>(this.generator, this.addFunc, this.empty);
        r = ConcurrentFactIndexer(self.generator, self.addFunc, self.empty)
# 		for (PredicateSym pred : this.coarseIdx.keySet()) {
        for pred in self.coarseIdx.keys():
# 			r.addAll(this.indexInto(pred));
            r.addAll_facts(self.indexInto_predsym(pred))
# 		}
# 		return r;
        return r
# 	}
#
# 	@Override
# 	public Set<PredicateSym> getPreds() {
# 		return this.coarseIdx.keySet();
# 	}
    def getPreds(self) -> Set[PredicateSym]:
        return set(self.coarseIdx.keys())
#
# 	/**
# 	 * Add all the facts from an indexable fact collection to this index.
# 	 *
# 	 * @param that
# 	 *            the indexable fact collection
# 	 */
# 	public void addAll(IndexableFactCollection that) {
    def addAll_indexable_fact_collection(self, that: IndexableFactCollection):
# 		for (PredicateSym pred : that.getPreds()) {
        for pred in that.getPreds():
# 			this.addAll(that.indexInto(pred));
            self.addAll_facts(that.indexInto_predsym(pred))
# 		}
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
# import java.util.Set;
# import java.util.concurrent.ConcurrentMap;
# import java.util.concurrent.atomic.AtomicReferenceArray;
# import java.util.function.BiConsumer;
# import java.util.function.Supplier;
#
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.Term;
# import abcdatalog.ast.visitors.TermVisitor;
# import abcdatalog.ast.visitors.TermVisitorBuilder;
# import abcdatalog.util.Utilities;
# import abcdatalog.util.substitution.ConstOnlySubstitution;
#
# /**
#  * An index that holds facts. The facts are indexed by predicate symbol and then
#  * by the constants in each argument position. The indexer is parameterized by
#  * the type of the container that ultimately holds the facts (i.e., all facts
#  * that belong to the same index are added to the same container).
#  *
#  * In the presence of multiple threads, the indexer can momentarily be in an
#  * inconsistent state. However, after the add method returns having been invoked
#  * with a fact f, the indexer will be consistent with respect to f, meaning that
#  * f is properly indexed and that it is visible as such to all threads. (This
#  * only holds, of course, if the provided container type is thread safe.)
#  *
#  * @param <T>
#  *            the container type
#  */
# public class ConcurrentFactIndexer<T extends Iterable<PositiveAtom>> implements FactIndexer {
# 	private final Supplier<T> generator;
# 	private final BiConsumer<T,PositiveAtom> addFunc;
# 	private final Supplier<T> empty;
#
# 	private final ConcurrentMap<PredicateSym, AtomicReferenceArray<ConcurrentMap<Constant, T>>> fineIdx = Utilities.createConcurrentMap();
# 	private final ConcurrentMap<PredicateSym, T> coarseIdx = Utilities.createConcurrentMap();
#
# 	/**
# 	 * Creates a new fact indexer.
# 	 *
# 	 * @param generator
# 	 *            an anonymous function that returns a container
# 	 * @param addFunc
# 	 *            an anonymous function that adds a fact to a container
# 	 */
# 	public ConcurrentFactIndexer(Supplier<T> generator, BiConsumer<T,PositiveAtom> addFunc) {
# 		this(generator, addFunc, generator);
# 	}
#
# 	/**
# 	 * Creates a new fact indexer.
# 	 *
# 	 * @param generator
# 	 *            an anonymous function that returns a container
# 	 * @param addFunc
# 	 *            an anonymous function that adds a fact to a container
# 	 * @param empty
# 	 *            an anonymous function that returns an empty container (such as
# 	 *            a static instance)
# 	 */
# 	public ConcurrentFactIndexer(Supplier<T> generator, BiConsumer<T,PositiveAtom> addFunc, Supplier<T> empty) {
# 		this.generator = generator;
# 		this.addFunc = addFunc;
# 		this.empty = empty;
# 	}
#
# 	/**
# 	 * Adds a fact to this indexer.
# 	 *
# 	 * @param fact
# 	 *            the fact
# 	 */
# 	public void add(PositiveAtom fact) {
# 		assert fact.isGround();
# 		T rough = this.coarseIdx.get(fact.getPred());
# 		if (rough == null) {
# 			rough = this.generator.get();
# 			T existing = this.coarseIdx.putIfAbsent(fact.getPred(), rough);
# 			if (existing != null) {
# 				rough = existing;
# 			}
# 		}
# 		this.addFunc.accept(rough, fact);
#
# 		AtomicReferenceArray<ConcurrentMap<Constant, T>> byPos = this.fineIdx.get(fact.getPred());
# 		if (byPos == null) {
# 			byPos = new AtomicReferenceArray<>(fact.getPred().getArity());
# 			AtomicReferenceArray<ConcurrentMap<Constant, T>> existing = this.fineIdx.putIfAbsent(fact.getPred(), byPos);
# 			if (existing != null) {
# 				byPos = existing;
# 			}
# 		}
# 		assert byPos != null;
#
# 		Term[] args = fact.getArgs();
# 		for (int i = 0; i < args.length; ++i) {
# 			ConcurrentMap<Constant, T> byConstant = byPos.get(i);
# 			if (byConstant == null) {
# 				byConstant = Utilities.createConcurrentMap();
# 				if (!byPos.compareAndSet(i, null, byConstant)) {
# 					byConstant = byPos.get(i);
# 				}
# 			}
# 			Constant key = (Constant) args[i];
# 			T n = byConstant.get(key);
# 			if (n == null) {
# 				n = this.generator.get();
# 				T existing = byConstant.putIfAbsent(key, n);
# 				if (existing != null) {
# 					n = existing;
# 				}
# 			}
# 			this.addFunc.accept(n, fact);
# 		}
# 	}
#
# 	/**
# 	 * Adds the facts to the index.
# 	 *
# 	 * @param facts
# 	 *            the facts
# 	 */
# 	public void addAll(Iterable<PositiveAtom> facts) {
# 		for (PositiveAtom a : facts) {
# 			this.add(a);
# 		}
# 	}
#
# 	@Override
# 	public T indexInto(PositiveAtom a) {
# 		return this.indexInto(a, null);
# 	}
#
# 	private static final TermVisitor<ConstOnlySubstitution, Constant> tv = (new TermVisitorBuilder<ConstOnlySubstitution, Constant>())
# 			.onConstant((c, s) -> c).onVariable((x, s) -> {
# 				if (s != null) {
# 					return s.get(x);
# 				}
# 				return null;
# 			}).orCrash();
#
# 	@Override
# 	public T indexInto(PositiveAtom a, ConstOnlySubstitution s) {
# 		AtomicReferenceArray<ConcurrentMap<Constant, T>> byPos = this.fineIdx.get(a.getPred());
# 		if (byPos == null) {
# 			return this.empty.get();
# 		}
#
# 		int bestIdx = -1;
# 		Term bestConst = null;
# 		int maxKeySetSize = -1;
# 		Term[] args = a.getArgs();
# 		for (int i = 0; i < args.length; ++i) {
# 			Term t = args[i];
# //			if (!(t instanceof DummyTerm) && (t instanceof Constant || (s != null && (t = s.get((Variable) t)) != null))) {
# 			if ((t = t.accept(tv, s)) != null) {
# 				ConcurrentMap<Constant, T> byConstant = byPos.get(i);
# 				if (byConstant != null) {
# 					if (!byConstant.containsKey(t)) {
# 						return this.empty.get();
# 					}
# 					int keySetSize = byConstant.size();
# 					if (keySetSize > maxKeySetSize) {
# 						maxKeySetSize = keySetSize;
# 						bestIdx = i;
# 						bestConst = t;
# 					}
# 				}
# 			}
# 		}
#
# 		if (bestIdx == -1) {
# 			return this.coarseIdx.get(a.getPred());
# 		}
#
# 		return byPos.get(bestIdx).get(bestConst);
# 	}
#
# 	@Override
# 	public T indexInto(PredicateSym pred) {
# 		T t = this.coarseIdx.get(pred);
# 		if (t == null) {
# 			t = this.empty.get();
# 		}
# 		return t;
# 	}
#
# 	/**
# 	 * Clears this index.
# 	 */
# 	public void clear() {
# 		this.fineIdx.clear();
# 		this.coarseIdx.clear();
# 	}
#
# 	@Override
# 	public boolean isEmpty() {
# 		return this.coarseIdx.isEmpty();
# 	}
#
# 	public ConcurrentFactIndexer<T> getCopy() {
# 		// Lazy man's copy function... probably be faster if we actually
# 		// recursed through data structure copying whole indices. On the other
# 		// hand, that might end up creating a new fact indexer with an
# 		// inconsistent state.
# 		ConcurrentFactIndexer<T> r = new ConcurrentFactIndexer<>(this.generator, this.addFunc, this.empty);
# 		for (PredicateSym pred : this.coarseIdx.keySet()) {
# 			r.addAll(this.indexInto(pred));
# 		}
# 		return r;
# 	}
#
# 	@Override
# 	public Set<PredicateSym> getPreds() {
# 		return this.coarseIdx.keySet();
# 	}
#
# 	/**
# 	 * Add all the facts from an indexable fact collection to this index.
# 	 *
# 	 * @param that
# 	 *            the indexable fact collection
# 	 */
# 	public void addAll(IndexableFactCollection that) {
# 		for (PredicateSym pred : that.getPreds()) {
# 			this.addAll(that.indexInto(pred));
# 		}
# 	}
#
# }
