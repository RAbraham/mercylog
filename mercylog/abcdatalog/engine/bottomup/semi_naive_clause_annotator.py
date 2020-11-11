from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.negated_atom import NegatedAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.term import Term
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
from mercylog.abcdatalog.ast.visitors.crash_premise_visitor import CrashPremiseVisitor
from mercylog.abcdatalog.ast.visitors.default_conjunct_visitor import DefaultConjunctVisitor
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from mercylog.abcdatalog.ast.visitors.premise_visitor_builder import PremiseVisitorBuilder
from mercylog.abcdatalog.util.box import Box
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom, Annotation
from typing import *

# PremiseVisitor<Set<Variable>, Double> scorer = new CrashPremiseVisitor<Set<Variable>, Double>() {
class LocalCrashPremiseVisitor(CrashPremiseVisitor):
#     @Override
#     public Double visit(AnnotatedAtom atom, Set<Variable> boundVars) {
#         int count = 0, total = 0;
#         for (Term t : atom.getArgs()) {
#             if (t instanceof Constant || boundVars.contains(t)) {
#                 ++count;
#             }
#             ++total;
#         }
#         return (total == 0) ? 1.0 : count / total;
#     }
#
    def visit_annotated_atom(self, atom: AnnotatedAtom, boundVars: Set[Variable]) -> float:
        count: int = 0
        total: int = 0
        t: Term
        for t in atom.getArgs():
            if isinstance(t, Constant) or t in boundVars:
                count += 1
            total += 1

        return 1.0 if (total == 0) else count / total

#     @Override
#     public Double visit(BinaryUnifier u, Set<Variable> boundVars) {
#         for (Term t : u.getArgsIterable()) {
#             if (t instanceof Constant || boundVars.contains(t)) {
#                 return Double.POSITIVE_INFINITY;
#             }
#         }
#         return Double.NEGATIVE_INFINITY;
#     }
#
#     @Override
    def visit_binary_unifier(self, u: BinaryUnifier, boundVars: Set[Variable]) -> float:
        t: Term
        for t in u.getArgsIterable():
            if isinstance(t, Constant) or t in boundVars:
                return float("inf")
        return float("-inf")




#     public Double visit(BinaryDisunifier u, Set<Variable> boundVars) {
#         for (Term t : u.getArgsIterable()) {
#             if (!(t instanceof Constant || boundVars.contains(t))) {
#                 return Double.NEGATIVE_INFINITY;
#             }
#         }
#         return Double.POSITIVE_INFINITY;
#     }
    def visit_binary_disunifier(self, u: BinaryDisunifier, boundVars: Set[Variable]) -> float:
        t: Term
        for t in u.get_args_iterable():
            if not (isinstance(t, Constant) or t in boundVars):
                return float('-inf')
        return float('inf')
#
#     @Override
#     public Double visit(NegatedAtom atom, Set<Variable> boundVars) {
#         for (Term t : atom.getArgs()) {
#             if (!(t instanceof Constant || boundVars.contains(t))) {
#                 return Double.NEGATIVE_INFINITY;
#             }
#         }
#         return Double.POSITIVE_INFINITY;
#     }
    def visit_negated_atom(self, atom: NegatedAtom, boundVars: Set[Variable]) -> float:
        t: Term
        for t in atom.getArgs():
            if not (isinstance(t, Constant) or t in boundVars):
                return float('-inf')
        return float('inf')


# };


# PremiseVisitor<Set<Variable>, Void> boundVarUpdater = new DefaultConjunctVisitor<Set<Variable>, Void>() {
class LocalDefaultConjunctVisitor(DefaultConjunctVisitor):
#     @Override
#     public Void visit(AnnotatedAtom atom, Set<Variable> boundVars) {
#         for (Term t : atom.getArgs()) {
#             if (t instanceof Variable) {
#                 boundVars.add((Variable) t);
#             }
#         }
#         return null;
#     }

    def visit_annotated_atom(self, atom: AnnotatedAtom, boundVars: Set[Variable]) -> None:
        t: Term
        for t in atom.getArgs():
            if isinstance(t, Variable):
                boundVars.add(t)
        return None
#
#     @Override
#     public Void visit(BinaryUnifier u, Set<Variable> boundVars) {
#         for (Term t : u.getArgsIterable()) {
#             if (t instanceof Variable) {
#                 boundVars.add((Variable) t);
#             }
#         }
#         return null;
#     }
# };
    def visit_binary_unifier(self, u: BinaryUnifier, boundVars: Set[Variable]) -> None:
        # TODO: Duplication with above visit method
        t: Term
        for t in u.getArgsIterable():
            if isinstance(t, Variable):
                boundVars.add(t)
        return None


# 	public static final class SemiNaiveClause extends Clause {
class SemiNaiveClause(Clause):
#
# 		private SemiNaiveClause(Head head, List<Premise> body) {
    def __init__(self, head: Head, body: List[Premise]):
# 			super(head, body);
        super(SemiNaiveClause, self).__init__(head, body)
# 			if (body.isEmpty()) {
# 				throw new IllegalArgumentException("Body must not be empty.");
# 			}
        if not body:
            raise ValueError("Body must not be empty")
# 		}
#
# 		public AnnotatedAtom getFirstAtom() {
# 			assert body.get(0) instanceof AnnotatedAtom;
# 			return (AnnotatedAtom) body.get(0);
# 		}
    def getFirstAtom(self) -> AnnotatedAtom:
        assert isinstance(self.body[0], AnnotatedAtom)
        return self.body[0]
#
# 	}
#
# }


# /**
#  * A class for annotating a clause with annotations helpful for semi-naive
#  * evaluation.
#  *
#  */
# public class SemiNaiveClauseAnnotator {
class SemiNaiveClauseAnnotator:
# 	private final Set<PredicateSym> idbPreds;
    def __init__(self, idbPreds: Set[PredicateSym]):
        self.idbPreds = idbPreds
#
# 	public SemiNaiveClauseAnnotator(Set<PredicateSym> idbPreds) {
# 		this.idbPreds = idbPreds;
# 	}
#
# 	/**
# 	 * Returns a set of annotated clauses for a given unannotated clause. If the
# 	 * given clause only contains atoms with EDB predicate symbols, the
# 	 * resulting set will be a singleton. Otherwise, the cardinality of the
# 	 * return set will be equal to the number of atoms in the body of the clause
# 	 * that have IDB predicate symbols. Each returned clause is ordered so that
# 	 * it can be evaluated from left to right.
# 	 *
# 	 * @param original
# 	 *            the unannotated clause
# 	 * @return a set of annotated clauses
# 	 */
# 	public Set<SemiNaiveClause> annotate(ValidClause original) {
    def annotate_single(self, original: ValidClause) -> Set[SemiNaiveClause]:
# 		List<Premise> body = original.getBody();
        body: Tuple[Premise] = original.getBody()
# 		if (body.isEmpty()) {
# 			throw new IllegalArgumentException("Cannot annotate a bodiless clause.");
# 		}
        if not body:
            raise ValueError("Cannot annotate a bodiless clause")
# 		List<Premise> body2 = new ArrayList<>();
        body2: List[Premise] = []
# 		List<Integer> idbPositions = new ArrayList<>();
        idbPositions: List[int] = []
# 		Box<Integer> edbPos = new Box<>();
        edbPos: Box[int] = Box()
# 		PremiseVisitor<Integer, Void> findIdbs = (new PremiseVisitorBuilder<Integer, Void>())
# 				.onPositiveAtom((atom, pos) -> {
# 					if (idbPreds.contains(atom.getPred())) {
# 						idbPositions.add(pos);
# 						body2.add(atom);
# 					} else {
# 						if (edbPos.value == null) {
# 							edbPos.value = pos;
# 						}
# 						body2.add(new AnnotatedAtom(atom, AnnotatedAtom.Annotation.EDB));
# 					}
# 					return null;
# 				}).or((premise, ignore) -> {
# 					body2.add(premise);
# 					return null;
# 				});
#
        def add_to_body2(atom, pos):
            if atom.getPred() in self.idbPreds:
                idbPositions.append(pos)
                body2.append(atom)
            else:
                if not edbPos.value:
                    edbPos.value = pos
                    body2.append(AnnotatedAtom(atom, Annotation.EDB))
            return None
        def simple_add_to_body2(premise, ignore):
            body2.append(premise)

        findIdbs: PremiseVisitor[int, None] = PremiseVisitorBuilder().onPositiveAtom(add_to_body2).or_(simple_add_to_body2)
 		# int pos = 0;
        pos: int = 0
        c: Premise
# 		for (Premise c : body) {
# 			c.accept(findIdbs, pos++);
# 		}
        for c in body:
            pos += 1
            c.accept_premise_visitor(findIdbs, pos)
# 		body = body2;
        body = tuple(body2)
#
# 		if (idbPositions.isEmpty()) {
# 			if (edbPos.value == null) {
# 				edbPos.value = 0;
# 			}
# 			return Collections.singleton(sort(new Clause(original.getHead(), body), edbPos.value));
# 		}
#
        if not idbPositions:
            if not edbPos.value:
                edbPos.value = 0
            singleton_set = set()
            singleton_set.add(SemiNaiveClauseAnnotator.sort(Clause(original.getHead(), body), edbPos.value))
            assert len(singleton_set) == 1, 'Supposed to be a singleton set'
            return singleton_set

# 		Set<SemiNaiveClause> r = new HashSet<>();
        r: Set[SemiNaiveClause] = set()
        def add1(l_newBody: List, atom, anno):
            l_newBody.append(AnnotatedAtom(atom, anno))
            return None
        def add2(l_newBody: List, premise, ignore):
            l_newBody.append(premise)
            return None
# 		for (Integer i : idbPositions) {
        i: int
        for i in idbPositions:
# 			List<Premise> newBody = new ArrayList<>();
            newBody: List[Premise] = []
# 			PremiseVisitor<AnnotatedAtom.Annotation, Void> annotator = (new PremiseVisitorBuilder<AnnotatedAtom.Annotation, Void>())
#           aaa. This is difficult as newBody is within the for loop so it's initiallized all the time. Maybe we'll have to initialize it twice, once outside the loop and once inside again? Then we'll be able to create the functions outside the for loop
            add1_l = lambda atom, anno: add1(newBody, atom, anno)
            add2_l = lambda premise, ignore: add2(newBody, premise, ignore)
            annotator: PremiseVisitor[Annotation, None] = PremiseVisitorBuilder().onPositiveAtom(add1_l).or_(add2_l)
# 					.onPositiveAtom((atom, anno) -> {
# 						newBody.add(new AnnotatedAtom(atom, anno));
# 						return null;
# 					}).or((premise, ignore) -> {
# 						newBody.add(premise);
# 						return null;
# 					});

# 			Iterator<Premise> it = body.iterator();
# 			for (int j = 0; j < i; ++j) {
# 				it.next().accept(annotator, AnnotatedAtom.Annotation.IDB);
# 			}
            it = iter(body)
            item = None
            for j, _ in enumerate(body):
                if j >= i:
                    break
                item = next(it)
                item.accept_premise_visitor(annotator, Annotation.IDB)


# 			it.next().accept(annotator, AnnotatedAtom.Annotation.DELTA);
            item = next(it)
            item.accept_premise_visitor(annotator, Annotation.DELTA)
# 			while (it.hasNext()) {
# 				it.next().accept(annotator, AnnotatedAtom.Annotation.IDB_PREV);
# 			}
            while True:
                try:
                    item = next(it)
                    item.accept_premise_visitor(annotator, Annotation.IDB_PREV)
                except StopIteration:
                    break
# 			r.add(sort(new Clause(original.getHead(), newBody), i));
            r.add(SemiNaiveClauseAnnotator.sort(Clause(original.getHead(), tuple(newBody)), i))
# 		}
        return r
# 		return r;
# 	}
#
# 	public Set<SemiNaiveClause> annotate(Set<ValidClause> clauses) {
# 		Set<SemiNaiveClause> r = new HashSet<>();
# 		for (ValidClause clause : clauses) {
# 			r.addAll(annotate(clause));
# 		}
# 		return r;
# 	}
    def annotate_many(self, clauses: Set[ValidClause]) -> Set[SemiNaiveClause]:
        r: Set[SemiNaiveClause] = set()
        clause: ValidClause
        for clause in clauses:
            for a in self.annotate_single(clause):
                r.add(a)
        return r
#
# 	private static SemiNaiveClause sort(Clause original, int firstConjunctPos) {
    @staticmethod
    def sort(original: Clause, firstConjunctPos: int) -> SemiNaiveClause:
# 		List<Premise> body = new ArrayList<>(original.getBody());
        body: List[Premise] = list(original.getBody())
# 		if (body.isEmpty()) {
# 			return new SemiNaiveClause(original.getHead(), body);
# 		}
        if not body:
            return SemiNaiveClause(original.getHead(), body)
# 		PremiseVisitor<Set<Variable>, Void> boundVarUpdater = new DefaultConjunctVisitor<Set<Variable>, Void>() {

        boundVarUpdate: PremiseVisitor[Set[Variable]] = LocalDefaultConjunctVisitor()
# 			@Override
# 			public Void visit(AnnotatedAtom atom, Set<Variable> boundVars) {
# 				for (Term t : atom.getArgs()) {
# 					if (t instanceof Variable) {
# 						boundVars.add((Variable) t);
# 					}
# 				}
# 				return null;
# 			}
#
# 			@Override
# 			public Void visit(BinaryUnifier u, Set<Variable> boundVars) {
# 				for (Term t : u.getArgsIterable()) {
# 					if (t instanceof Variable) {
# 						boundVars.add((Variable) t);
# 					}
# 				}
# 				return null;
# 			}
# 		};
#


# 		PremiseVisitor<Set<Variable>, Double> scorer = new CrashPremiseVisitor<Set<Variable>, Double>() {
        scorer: PremiseVisitor[Set[Variable], float] = LocalCrashPremiseVisitor()
# 			@Override
# 			public Double visit(AnnotatedAtom atom, Set<Variable> boundVars) {
# 				int count = 0, total = 0;
# 				for (Term t : atom.getArgs()) {
# 					if (t instanceof Constant || boundVars.contains(t)) {
# 						++count;
# 					}
# 					++total;
# 				}
# 				return (total == 0) ? 1.0 : count / total;
# 			}
#
# 			@Override
# 			public Double visit(BinaryUnifier u, Set<Variable> boundVars) {
# 				for (Term t : u.getArgsIterable()) {
# 					if (t instanceof Constant || boundVars.contains(t)) {
# 						return Double.POSITIVE_INFINITY;
# 					}
# 				}
# 				return Double.NEGATIVE_INFINITY;
# 			}
#
# 			@Override
# 			public Double visit(BinaryDisunifier u, Set<Variable> boundVars) {
# 				for (Term t : u.getArgsIterable()) {
# 					if (!(t instanceof Constant || boundVars.contains(t))) {
# 						return Double.NEGATIVE_INFINITY;
# 					}
# 				}
# 				return Double.POSITIVE_INFINITY;
# 			}
#
# 			@Override
# 			public Double visit(NegatedAtom atom, Set<Variable> boundVars) {
# 				for (Term t : atom.getArgs()) {
# 					if (!(t instanceof Constant || boundVars.contains(t))) {
# 						return Double.NEGATIVE_INFINITY;
# 					}
# 				}
# 				return Double.POSITIVE_INFINITY;
# 			}
# 		};
#
        aaa
# 		Collections.swap(body, 0, firstConjunctPos);
# 		int size = body.size();
# 		Set<Variable> boundVars = new HashSet<>();
# 		for (int i = 1; i < size; ++i) {
# 			body.get(i - 1).accept(boundVarUpdater, boundVars);
# 			int bestPos = -1;
# 			double bestScore = Double.NEGATIVE_INFINITY;
# 			for (int j = i; j < size; ++j) {
# 				Double score = body.get(j).accept(scorer, boundVars);
# 				if (score > bestScore) {
# 					bestScore = score;
# 					bestPos = j;
# 				}
# 			}
# 			assert bestPos != -1;
# 			Collections.swap(body, i, bestPos);
# 		}
#
# 		return new SemiNaiveClause(original.getHead(), body);
# 	}
#

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
# import java.util.ArrayList;
# import java.util.Collections;
# import java.util.HashSet;
# import java.util.Iterator;
# import java.util.List;
# import java.util.Set;
#
# import abcdatalog.ast.BinaryDisunifier;
# import abcdatalog.ast.BinaryUnifier;
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.Constant;
# import abcdatalog.ast.Head;
# import abcdatalog.ast.NegatedAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.Premise;
# import abcdatalog.ast.Term;
# import abcdatalog.ast.Variable;
# import abcdatalog.ast.validation.DatalogValidator.ValidClause;
# import abcdatalog.ast.visitors.CrashPremiseVisitor;
# import abcdatalog.ast.visitors.DefaultConjunctVisitor;
# import abcdatalog.ast.visitors.PremiseVisitor;
# import abcdatalog.ast.visitors.PremiseVisitorBuilder;
# import abcdatalog.util.Box;
#
# /**
#  * A class for annotating a clause with annotations helpful for semi-naive
#  * evaluation.
#  *
#  */
# public class SemiNaiveClauseAnnotator {
# 	private final Set<PredicateSym> idbPreds;
#
# 	public SemiNaiveClauseAnnotator(Set<PredicateSym> idbPreds) {
# 		this.idbPreds = idbPreds;
# 	}
#
# 	/**
# 	 * Returns a set of annotated clauses for a given unannotated clause. If the
# 	 * given clause only contains atoms with EDB predicate symbols, the
# 	 * resulting set will be a singleton. Otherwise, the cardinality of the
# 	 * return set will be equal to the number of atoms in the body of the clause
# 	 * that have IDB predicate symbols. Each returned clause is ordered so that
# 	 * it can be evaluated from left to right.
# 	 *
# 	 * @param original
# 	 *            the unannotated clause
# 	 * @return a set of annotated clauses
# 	 */
# 	public Set<SemiNaiveClause> annotate(ValidClause original) {
# 		List<Premise> body = original.getBody();
# 		if (body.isEmpty()) {
# 			throw new IllegalArgumentException("Cannot annotate a bodiless clause.");
# 		}
# 		List<Premise> body2 = new ArrayList<>();
# 		List<Integer> idbPositions = new ArrayList<>();
# 		Box<Integer> edbPos = new Box<>();
# 		PremiseVisitor<Integer, Void> findIdbs = (new PremiseVisitorBuilder<Integer, Void>())
# 				.onPositiveAtom((atom, pos) -> {
# 					if (idbPreds.contains(atom.getPred())) {
# 						idbPositions.add(pos);
# 						body2.add(atom);
# 					} else {
# 						if (edbPos.value == null) {
# 							edbPos.value = pos;
# 						}
# 						body2.add(new AnnotatedAtom(atom, AnnotatedAtom.Annotation.EDB));
# 					}
# 					return null;
# 				}).or((premise, ignore) -> {
# 					body2.add(premise);
# 					return null;
# 				});
# 		int pos = 0;
# 		for (Premise c : body) {
# 			c.accept(findIdbs, pos++);
# 		}
# 		body = body2;
#
# 		if (idbPositions.isEmpty()) {
# 			if (edbPos.value == null) {
# 				edbPos.value = 0;
# 			}
# 			return Collections.singleton(sort(new Clause(original.getHead(), body), edbPos.value));
# 		}
#
# 		Set<SemiNaiveClause> r = new HashSet<>();
# 		for (Integer i : idbPositions) {
# 			List<Premise> newBody = new ArrayList<>();
# 			PremiseVisitor<AnnotatedAtom.Annotation, Void> annotator = (new PremiseVisitorBuilder<AnnotatedAtom.Annotation, Void>())
# 					.onPositiveAtom((atom, anno) -> {
# 						newBody.add(new AnnotatedAtom(atom, anno));
# 						return null;
# 					}).or((premise, ignore) -> {
# 						newBody.add(premise);
# 						return null;
# 					});
# 			Iterator<Premise> it = body.iterator();
# 			for (int j = 0; j < i; ++j) {
# 				it.next().accept(annotator, AnnotatedAtom.Annotation.IDB);
# 			}
# 			it.next().accept(annotator, AnnotatedAtom.Annotation.DELTA);
# 			while (it.hasNext()) {
# 				it.next().accept(annotator, AnnotatedAtom.Annotation.IDB_PREV);
# 			}
# 			r.add(sort(new Clause(original.getHead(), newBody), i));
# 		}
# 		return r;
# 	}
#
# 	public Set<SemiNaiveClause> annotate(Set<ValidClause> clauses) {
# 		Set<SemiNaiveClause> r = new HashSet<>();
# 		for (ValidClause clause : clauses) {
# 			r.addAll(annotate(clause));
# 		}
# 		return r;
# 	}
#
# 	private static SemiNaiveClause sort(Clause original, int firstConjunctPos) {
# 		List<Premise> body = new ArrayList<>(original.getBody());
# 		if (body.isEmpty()) {
# 			return new SemiNaiveClause(original.getHead(), body);
# 		}
# 		PremiseVisitor<Set<Variable>, Void> boundVarUpdater = new DefaultConjunctVisitor<Set<Variable>, Void>() {
# 			@Override
# 			public Void visit(AnnotatedAtom atom, Set<Variable> boundVars) {
# 				for (Term t : atom.getArgs()) {
# 					if (t instanceof Variable) {
# 						boundVars.add((Variable) t);
# 					}
# 				}
# 				return null;
# 			}
#
# 			@Override
# 			public Void visit(BinaryUnifier u, Set<Variable> boundVars) {
# 				for (Term t : u.getArgsIterable()) {
# 					if (t instanceof Variable) {
# 						boundVars.add((Variable) t);
# 					}
# 				}
# 				return null;
# 			}
# 		};
#
# 		PremiseVisitor<Set<Variable>, Double> scorer = new CrashPremiseVisitor<Set<Variable>, Double>() {
# 			@Override
# 			public Double visit(AnnotatedAtom atom, Set<Variable> boundVars) {
# 				int count = 0, total = 0;
# 				for (Term t : atom.getArgs()) {
# 					if (t instanceof Constant || boundVars.contains(t)) {
# 						++count;
# 					}
# 					++total;
# 				}
# 				return (total == 0) ? 1.0 : count / total;
# 			}
#
# 			@Override
# 			public Double visit(BinaryUnifier u, Set<Variable> boundVars) {
# 				for (Term t : u.getArgsIterable()) {
# 					if (t instanceof Constant || boundVars.contains(t)) {
# 						return Double.POSITIVE_INFINITY;
# 					}
# 				}
# 				return Double.NEGATIVE_INFINITY;
# 			}
#
# 			@Override
# 			public Double visit(BinaryDisunifier u, Set<Variable> boundVars) {
# 				for (Term t : u.getArgsIterable()) {
# 					if (!(t instanceof Constant || boundVars.contains(t))) {
# 						return Double.NEGATIVE_INFINITY;
# 					}
# 				}
# 				return Double.POSITIVE_INFINITY;
# 			}
#
# 			@Override
# 			public Double visit(NegatedAtom atom, Set<Variable> boundVars) {
# 				for (Term t : atom.getArgs()) {
# 					if (!(t instanceof Constant || boundVars.contains(t))) {
# 						return Double.NEGATIVE_INFINITY;
# 					}
# 				}
# 				return Double.POSITIVE_INFINITY;
# 			}
# 		};
#
# 		Collections.swap(body, 0, firstConjunctPos);
# 		int size = body.size();
# 		Set<Variable> boundVars = new HashSet<>();
# 		for (int i = 1; i < size; ++i) {
# 			body.get(i - 1).accept(boundVarUpdater, boundVars);
# 			int bestPos = -1;
# 			double bestScore = Double.NEGATIVE_INFINITY;
# 			for (int j = i; j < size; ++j) {
# 				Double score = body.get(j).accept(scorer, boundVars);
# 				if (score > bestScore) {
# 					bestScore = score;
# 					bestPos = j;
# 				}
# 			}
# 			assert bestPos != -1;
# 			Collections.swap(body, i, bestPos);
# 		}
#
# 		return new SemiNaiveClause(original.getHead(), body);
# 	}
#
# 	public static final class SemiNaiveClause extends Clause {
#
# 		private SemiNaiveClause(Head head, List<Premise> body) {
# 			super(head, body);
# 			if (body.isEmpty()) {
# 				throw new IllegalArgumentException("Body must not be empty.");
# 			}
# 		}
#
# 		public AnnotatedAtom getFirstAtom() {
# 			assert body.get(0) instanceof AnnotatedAtom;
# 			return (AnnotatedAtom) body.get(0);
# 		}
#
# 	}
#
# }
