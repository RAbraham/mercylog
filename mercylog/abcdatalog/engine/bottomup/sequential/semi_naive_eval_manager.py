from typing import *
# import abcdatalog.ast.Clause;
from mercylog.abcdatalog.ast.clause import Clause
# import abcdatalog.ast.PositiveAtom;
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
# import abcdatalog.ast.PredicateSym;
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
# import abcdatalog.ast.Premise;
from mercylog.abcdatalog.ast.premise import Premise
# import abcdatalog.ast.validation.DatalogValidationException;
from mercylog.abcdatalog.ast.validation.datalog_validation_exception import DatalogValidationException
# import abcdatalog.ast.validation.DatalogValidator;
from mercylog.abcdatalog.ast.validation.datalog_validator import  DatalogValidator
# import abcdatalog.ast.validation.StratifiedNegationValidator;
from mercylog.abcdatalog.ast.validation.stratified_negation_validator import StratifiedNegationValidator
# import abcdatalog.ast.validation.StratifiedProgram;
from mercylog.abcdatalog.ast.validation.stratified_program import StratifiedProgram
# import abcdatalog.ast.validation.DatalogValidator.ValidClause;
from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
# import abcdatalog.ast.validation.UnstratifiedProgram;
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
# import abcdatalog.ast.visitors.HeadVisitor;
from mercylog.abcdatalog.ast.visitors.head_visitor import HeadVisitor
# import abcdatalog.ast.visitors.PremiseVisitor;
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
# import abcdatalog.ast.visitors.PremiseVisitorBuilder;
from mercylog.abcdatalog.ast.visitors.premise_visitor_builder import PremiseVisitorBuilder
# import abcdatalog.engine.bottomup.AnnotatedAtom;
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom
# import abcdatalog.engine.bottomup.ClauseEvaluator;
from mercylog.abcdatalog.engine.bottomup.clause_evaluator import ClauseEvaluator
# import abcdatalog.engine.bottomup.EvalManager;
from mercylog.abcdatalog.engine.bottomup.eval_manager import EvalManager
# import abcdatalog.engine.bottomup.SemiNaiveClauseAnnotator;
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClauseAnnotator
# import abcdatalog.engine.bottomup.SemiNaiveClauseAnnotator.SemiNaiveClause;
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClause
from mercylog.abcdatalog.util.utilities import Utilities
# import abcdatalog.util.datastructures.ConcurrentFactIndexer;
from mercylog.abcdatalog.util.datastructures.concurrent_fact_indexer import ConcurrentFactIndexer
# import abcdatalog.util.datastructures.FactIndexer;
from mercylog.abcdatalog.util.datastructures.fact_indexer import FactIndexer
# import abcdatalog.util.datastructures.FactIndexerFactory;
from mercylog.abcdatalog.util.datastructures.fact_indexer_factory import FactIndexerFactory
# import abcdatalog.util.datastructures.IndexableFactCollection;
from mercylog.abcdatalog.util.datastructures.indexable_fact_collection import IndexableFactCollection
# import abcdatalog.util.substitution.ClauseSubstitution;
from mercylog.abcdatalog.util.substitution.clause_substitution import ClauseSubstitution
from mercylog.abcdatalog.engine.bottomup.annotated_atom import Annotation


# private class StratumEvaluator {
class StratumEvaluator:
#     private ConcurrentFactIndexer<Set<PositiveAtom>> idbsPrev = FactIndexerFactory
#             .createConcurrentSetFactIndexer();
#     private ConcurrentFactIndexer<Set<PositiveAtom>> deltaOld = FactIndexerFactory
#             .createConcurrentSetFactIndexer();
#     private ConcurrentFactIndexer<Set<PositiveAtom>> deltaNew = FactIndexerFactory
#             .createConcurrentSetFactIndexer();
#     private final Map<PredicateSym, Set<ClauseEvaluator>> firstRoundEvals;
#     private final Map<PredicateSym, Set<ClauseEvaluator>> laterRoundEvals;
#     private final Set<PositiveAtom> initialIdbFacts;
#
#     public StratumEvaluator(Map<PredicateSym, Set<SemiNaiveClause>> firstRoundRules,
#         Map<PredicateSym, Set<SemiNaiveClause>> laterRoundRules, Set<PositiveAtom> initialIdbFacts) {

    def __init__(self, firstRoundRules: Dict[PredicateSym, Set[SemiNaiveClause]], laterRoundRules: Dict[PredicateSym, Set[SemiNaiveClause]], initialIdbFacts, allFacts):
        #     Function<Map<PredicateSym, Set<SemiNaiveClause>>, Map<PredicateSym, Set<ClauseEvaluator>>> translate = (
        #             clauseMap) -> {
        #         Map<PredicateSym, Set<ClauseEvaluator>> evalMap = new HashMap<>();
        #         for (Map.Entry<PredicateSym, Set<SemiNaiveClause>> entry : clauseMap.entrySet()) {
        #             Set<ClauseEvaluator> s = new HashSet<>();
        #             for (SemiNaiveClause cl : entry.getValue()) {
        #                 s.add(new ClauseEvaluator(cl, this::addFact, this::getFacts));
        #             }
        #             evalMap.put(entry.getKey(), s);
        #         }
        #         return evalMap;
        #     };
        def translate(clauseMap):
            evalMap: Dict[PredicateSym, Set[ClauseEvaluator]] = dict()
            entry: Tuple[PredicateSym, Set[SemiNaiveClause]]
            for entry in clauseMap.items():
                s: Set[ClauseEvaluator] = set()
                cl: SemiNaiveClause
                for cl in entry[1]:
                    s.add(ClauseEvaluator(cl, self.addFact, self.getFacts))
                evalMap[entry[0]] = s
            return evalMap


#     firstRoundEvals = translate.apply(firstRoundRules);
        self.firstRoundEvals = translate(firstRoundRules)
#     laterRoundEvals = translate.apply(laterRoundRules);
        self.laterRoundEvals = translate(laterRoundRules)
        self.initialIdbFacts: Set[PositiveAtom] = initialIdbFacts
        self.deltaNew: ConcurrentFactIndexer = FactIndexerFactory.createConcurrentSetFactIndexer()
        self.deltaOld: ConcurrentFactIndexer = FactIndexerFactory.createConcurrentSetFactIndexer()
        self.idbsPrev: ConcurrentFactIndexer = FactIndexerFactory.createConcurrentSetFactIndexer()
        self.allFacts = allFacts
# }
#
#     public void eval() {
    def eval(self):
#         deltaNew.addAll(this.initialIdbFacts);
#         evalOneRound(allFacts, firstRoundEvals);
#         while (evalOneRound(deltaOld, laterRoundEvals)) {
#             // Loop...
#         }
        self.deltaNew.addAll(self.initialIdbFacts)
        self.evalOneRound(self.allFacts, self.firstRoundEvals)
        while self.evalOneRound(self.deltaOld, self.laterRoundEvals):
            pass
#     }
#
#     private boolean evalOneRound(FactIndexer index, Map<PredicateSym, Set<ClauseEvaluator>> rules) {
    def evalOneRound(self, index: FactIndexer, rules: Dict[PredicateSym, Set[ClauseEvaluator]]) -> bool:
#         for (PredicateSym pred : index.getPreds()) {
#             Set<ClauseEvaluator> evals = rules.get(pred);
#             if (evals != null) {
#                 for (ClauseEvaluator eval : evals) {
#                     for (PositiveAtom fact : index.indexInto(pred)) {
#                         eval.evaluate(fact);
#                     }
#                 }
#             }
#         }
#
        for pred in index.getPreds():
            evals: Set[ClauseEvaluator] = rules.get(pred)
            if evals is not None:
                eval: ClauseEvaluator
                for eval in evals:
                    for fact in index.indexInto_predsym(pred):
                        eval.evaluate(fact)
                pass
#         if (deltaNew.isEmpty()) {
#             return false;
#         }
        if self.deltaNew.isEmpty():
            return False
#
#         idbsPrev.addAll(deltaOld);
#         allFacts.addAll(deltaNew);
#         deltaOld = deltaNew;
#         deltaNew = FactIndexerFactory.createConcurrentSetFactIndexer();
#         return true;

        self.idbsPrev.addAll(self.deltaOld)
        self.allFacts.addAll(self.deltaNew)
        self.deltaOld = self.deltaNew
        self.deltaNew = FactIndexerFactory.createConcurrentSetFactIndexer()
        return True
#     }
#
#     private boolean addFact(PositiveAtom fact, ClauseSubstitution subst) {
#         fact = fact.applySubst(subst);
#         Set<PositiveAtom> set = allFacts.indexInto(fact);
#         if (!set.contains(fact)) {
#             deltaNew.add(fact);
#             return true;
#         }
#         return false;
#     }
#
    def addFact(self, fact: PositiveAtom, subst: ClauseSubstitution) -> bool:
        fact = fact.applySubst(subst)
        a_set: Set[PositiveAtom] = self.allFacts.indexInto(fact)
        if fact not in a_set:
            self.deltaNew.add(fact)
            return True
        return False

#     private Iterable<PositiveAtom> getFacts(AnnotatedAtom atom, ClauseSubstitution subst) {
    def getFacts(self, atom: AnnotatedAtom, subst: ClauseSubstitution) -> Iterable[PositiveAtom]:
#         Set<PositiveAtom> r = null;
#         PositiveAtom unannotated = atom.asUnannotatedAtom();
#         switch (atom.getAnnotation()) {
#         case EDB:
#             // Fall through...
#         case IDB:
#             r = allFacts.indexInto(unannotated, subst);
#             break;
#         case IDB_PREV:
#             r = idbsPrev.indexInto(unannotated, subst);
#             break;
#         case DELTA:
#             r = deltaOld.indexInto(unannotated, subst);
#             break;
#         default:
#             assert false;
#         }
#         return r;
        r: Optional[Set[PositiveAtom]] = None
        unannotated: PositiveAtom = atom.asUnannotatedAtom()
        annotation = atom.getAnnotation()
        if annotation == Annotation.IDB:
            r = self.allFacts.indexInto(unannotated, subst)
        elif annotation == Annotation.IDB_PREV:
            r = self.idbsPrev.indexInto_patom_with_substitution(unannotated, subst)
        elif annotation == Annotation.DELTA:
            r = self.deltaOld.indexInto_patom_with_substitution(unannotated, subst)
        return r
#     }
# }



# HeadVisitor<Void, PredicateSym> getHeadPred = new HeadVisitor<Void, PredicateSym>() {
class LocalHeadVisitor(HeadVisitor):
    def __init__(self):
        super(LocalHeadVisitor, self).__init__()
#     @Override
#     public PredicateSym visit(PositiveAtom atom, Void state) {
    def visit(self, atom: PositiveAtom, state) -> PredicateSym:
#         return atom.getPred();
        return atom.getPred()
#     }
#
# };
# public class SemiNaiveEvalManager implements EvalManager {
class SemiNaiveEvalManager(EvalManager):
# 	private final ConcurrentFactIndexer<Set<PositiveAtom>> allFacts = FactIndexerFactory
# 			.createConcurrentSetFactIndexer();
# 	private final List<StratumEvaluator> stratumEvals = new ArrayList<>();
#
    def __init__(self):
        self.allFacts: ConcurrentFactIndexer[Set[PositiveAtom]] = FactIndexerFactory.createConcurrentSetFactIndexer()
        self.stratumEvals: List[StratumEvaluator] = []

# 	@SuppressWarnings("unchecked")
# 	@Override
# 	public synchronized void initialize(Set<Clause> program) throws DatalogValidationException {
    def initialize(self, program: Set[Clause]):
# 		UnstratifiedProgram prog = (new DatalogValidator()).withBinaryDisunificationInRuleBody()
# 				.withBinaryUnificationInRuleBody().withAtomNegationInRuleBody().validate(program);
        prog: UnstratifiedProgram = DatalogValidator().withBinaryDisunificationInRuleBody().withBinaryUnificationInRuleBody().withAtomNegationInRuleBody().validate(program)
# 		StratifiedProgram stratProg = StratifiedNegationValidator.validate(prog);
        stratProg: StratifiedProgram = StratifiedNegationValidator.validate(prog)

# 		List<Set<PredicateSym>> strata = stratProg.getStrata();
        strata: List[Set[PredicateSym]] = stratProg.getStrata()
# 		int nstrata = strata.size();
        nstrata = len(strata)
# 		Map<PredicateSym, Set<SemiNaiveClause>>[] firstRoundRules = new HashMap[nstrata];
        firstRoundRules: List[Dict[PredicateSym, Set[SemiNaiveClause]]] = []
# 		Map<PredicateSym, Set<SemiNaiveClause>>[] laterRoundRules = new HashMap[nstrata];
        laterRoundRules: List[Dict[PredicateSym, Set[SemiNaiveClause]]] = []
# 		Set<PositiveAtom>[] initialIdbFacts = new HashSet[nstrata];
        self.initialIdbFacts: List[Set[PositiveAtom]] = []
# 		for (int i = 0; i < nstrata; ++i) {
        for i in range(nstrata):
# 			firstRoundRules[i] = new HashMap<>();
            firstRoundRules[i] = dict()
# 			laterRoundRules[i] = new HashMap<>();
            laterRoundRules[i] = dict()
# 			initialIdbFacts[i] = new HashSet<>();
            self.initialIdbFacts[i] = set()
# 		}
# 		Map<PredicateSym, Integer> predToStratumMap = stratProg.getPredToStratumMap();
        predToStratumMap: Dict[PredicateSym, int] = stratProg.getPredToStratumMap()
#
# 		HeadVisitor<Void, PredicateSym> getHeadPred = new HeadVisitor<Void, PredicateSym>() {
        getHeadPred: HeadVisitor = LocalHeadVisitor()
# 			@Override
# 			public PredicateSym visit(PositiveAtom atom, Void state) {
# 				return atom.getPred();
# 			}
#
# 		};



# 		for (ValidClause clause : prog.getRules()) {
        for clause in prog.getRules():
# 			PredicateSym pred = clause.getHead().accept(getHeadPred, null);
            pred: PredicateSym = clause.getHead().accept_head_visitor(getHeadPred, None)
# 			int stratum = predToStratumMap.get(pred);
            stratum: int = predToStratumMap.get(pred)
# 			// Treat IDB predicates from earlier strata as EDB predicates.
# 			Set<PredicateSym> idbs = strata.get(stratum);
            idbs: Set[PredicateSym] = strata[stratum]
# 			PremiseVisitor<Boolean, Boolean> checkForIdbPred = (new PremiseVisitorBuilder<Boolean, Boolean>())
# 					.onPositiveAtom((atom, idb) -> idbs.contains(atom.getPred()) || idb).or((premise, idb) -> idb);
            patom_func = lambda atom, idb: atom.getPred() in idbs or idb
            checkForIdbPred: PremiseVisitor[bool, bool] = PremiseVisitorBuilder().onPositiveAtom(patom_func).or_(lambda premise, idb: idb)
# 			SemiNaiveClauseAnnotator annotator = new SemiNaiveClauseAnnotator(idbs);
            annotator: SemiNaiveClauseAnnotator = SemiNaiveClauseAnnotator(list(idbs))
# 			boolean hasIdbPred = false;
            hasIdbPred = False
# 			for (Premise c : clause.getBody()) {
            c: Premise
            for c in clause.getBody():
# 				hasIdbPred = c.accept(checkForIdbPred, hasIdbPred);
                hasIdbPred = c.accept_premise_visitor(checkForIdbPred, hasIdbPred)
# 			}

# 			for (SemiNaiveClause rule : annotator.annotate(clause)) {
            rule: SemiNaiveClause
            for rule in annotator.annotate_single(clause):
# 				PredicateSym bodyPred = rule.getFirstAtom().getPred();
                bodyPred: PredicateSym = rule.getFirstAtom().getPred()
# 				if (hasIdbPred) {
                if hasIdbPred:
# 					Utilities.getSetFromMap(laterRoundRules[stratum], bodyPred).add(rule);
                    Utilities.getSetFromMap(laterRoundRules[stratum], bodyPred).add(rule)
# 				} else {
                else:
# 					Utilities.getSetFromMap(firstRoundRules[stratum], bodyPred).add(rule);
                    Utilities.getSetFromMap(firstRoundRules[stratum], bodyPred).add(rule)
# 				}
# 			}
#
# 		}
#
# 		Set<PredicateSym> edbs = prog.getEdbPredicateSyms();
        edbs: Set[PredicateSym] = prog.getEdbPredicateSyms()
# 		for (PositiveAtom fact : prog.getInitialFacts()) {
        fact: PositiveAtom
        for fact in prog.getInitialFacts():
# 			if (edbs.contains(fact.getPred())) {
            if fact.getPred() in edbs:
# 				allFacts.add(fact);
                self.allFacts.add(fact)
# 			} else {
            else:
# 				initialIdbFacts[predToStratumMap.get(fact.getPred())].add(fact);
                self.initialIdbFacts[predToStratumMap.get(fact.getPred())].add(fact)
# 			}
# 		}
#
# 		for (int i = 0; i < nstrata; ++i) {
# 			stratumEvals.add(new StratumEvaluator(firstRoundRules[i], laterRoundRules[i], initialIdbFacts[i]));
# 		}
        for i in range(nstrata):
            self.stratumEvals.append(StratumEvaluator(firstRoundRules[i], laterRoundRules[i], self.initialIdbFacts[i], self.allFacts))
# 	}
#
# 	@Override
# 	public synchronized IndexableFactCollection eval() {
# 		for (StratumEvaluator se : stratumEvals) {
# 			se.eval();
# 		}
# 		return allFacts;
# 	}
#

    def eval(self) -> IndexableFactCollection:
        se: StratumEvaluator
        for se in self.stratumEvals:
            se.eval()
        return self.allFacts

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
#
# // import java.util.ArrayList;
# // import java.util.HashMap;
# // import java.util.HashSet;
# // import java.util.List;
# // import java.util.Map;
# // import java.util.Set;
# // import java.util.function.Function;
#
# import abcdatalog.ast.Clause;
# import abcdatalog.ast.PositiveAtom;
# import abcdatalog.ast.PredicateSym;
# import abcdatalog.ast.Premise;
# import abcdatalog.ast.validation.DatalogValidationException;
# import abcdatalog.ast.validation.DatalogValidator;
# import abcdatalog.ast.validation.StratifiedNegationValidator;
# import abcdatalog.ast.validation.StratifiedProgram;
# import abcdatalog.ast.validation.DatalogValidator.ValidClause;
# import abcdatalog.ast.validation.UnstratifiedProgram;
# import abcdatalog.ast.visitors.HeadVisitor;
# import abcdatalog.ast.visitors.PremiseVisitor;
# import abcdatalog.ast.visitors.PremiseVisitorBuilder;
# import abcdatalog.engine.bottomup.AnnotatedAtom;
# import abcdatalog.engine.bottomup.ClauseEvaluator;
# import abcdatalog.engine.bottomup.EvalManager;
# import abcdatalog.engine.bottomup.SemiNaiveClauseAnnotator;
# import abcdatalog.engine.bottomup.SemiNaiveClauseAnnotator.SemiNaiveClause;
# import abcdatalog.util.Utilities;
# import abcdatalog.util.datastructures.ConcurrentFactIndexer;
# import abcdatalog.util.datastructures.FactIndexer;
# import abcdatalog.util.datastructures.FactIndexerFactory;
# import abcdatalog.util.datastructures.IndexableFactCollection;
# import abcdatalog.util.substitution.ClauseSubstitution;
#
# public class SemiNaiveEvalManager implements EvalManager {
# 	private final ConcurrentFactIndexer<Set<PositiveAtom>> allFacts = FactIndexerFactory
# 			.createConcurrentSetFactIndexer();
# 	private final List<StratumEvaluator> stratumEvals = new ArrayList<>();
#
# 	@SuppressWarnings("unchecked")
# 	@Override
# 	public synchronized void initialize(Set<Clause> program) throws DatalogValidationException {
# 		UnstratifiedProgram prog = (new DatalogValidator()).withBinaryDisunificationInRuleBody()
# 				.withBinaryUnificationInRuleBody().withAtomNegationInRuleBody().validate(program);
# 		StratifiedProgram stratProg = StratifiedNegationValidator.validate(prog);
# 		List<Set<PredicateSym>> strata = stratProg.getStrata();
# 		int nstrata = strata.size();
# 		Map<PredicateSym, Set<SemiNaiveClause>>[] firstRoundRules = new HashMap[nstrata];
# 		Map<PredicateSym, Set<SemiNaiveClause>>[] laterRoundRules = new HashMap[nstrata];
# 		Set<PositiveAtom>[] initialIdbFacts = new HashSet[nstrata];
# 		for (int i = 0; i < nstrata; ++i) {
# 			firstRoundRules[i] = new HashMap<>();
# 			laterRoundRules[i] = new HashMap<>();
# 			initialIdbFacts[i] = new HashSet<>();
# 		}
# 		Map<PredicateSym, Integer> predToStratumMap = stratProg.getPredToStratumMap();
#
# 		HeadVisitor<Void, PredicateSym> getHeadPred = new HeadVisitor<Void, PredicateSym>() {
#
# 			@Override
# 			public PredicateSym visit(PositiveAtom atom, Void state) {
# 				return atom.getPred();
# 			}
#
# 		};
# 		for (ValidClause clause : prog.getRules()) {
# 			PredicateSym pred = clause.getHead().accept(getHeadPred, null);
# 			int stratum = predToStratumMap.get(pred);
# 			// Treat IDB predicates from earlier strata as EDB predicates.
# 			Set<PredicateSym> idbs = strata.get(stratum);
# 			PremiseVisitor<Boolean, Boolean> checkForIdbPred = (new PremiseVisitorBuilder<Boolean, Boolean>())
# 					.onPositiveAtom((atom, idb) -> idbs.contains(atom.getPred()) || idb).or((premise, idb) -> idb);
# 			SemiNaiveClauseAnnotator annotator = new SemiNaiveClauseAnnotator(idbs);
# 			boolean hasIdbPred = false;
# 			for (Premise c : clause.getBody()) {
# 				hasIdbPred = c.accept(checkForIdbPred, hasIdbPred);
# 			}
# 			for (SemiNaiveClause rule : annotator.annotate(clause)) {
# 				PredicateSym bodyPred = rule.getFirstAtom().getPred();
# 				if (hasIdbPred) {
# 					Utilities.getSetFromMap(laterRoundRules[stratum], bodyPred).add(rule);
# 				} else {
# 					Utilities.getSetFromMap(firstRoundRules[stratum], bodyPred).add(rule);
# 				}
# 			}
#
# 		}
#
# 		Set<PredicateSym> edbs = prog.getEdbPredicateSyms();
# 		for (PositiveAtom fact : prog.getInitialFacts()) {
# 			if (edbs.contains(fact.getPred())) {
# 				allFacts.add(fact);
# 			} else {
# 				initialIdbFacts[predToStratumMap.get(fact.getPred())].add(fact);
# 			}
# 		}
#
# 		for (int i = 0; i < nstrata; ++i) {
# 			stratumEvals.add(new StratumEvaluator(firstRoundRules[i], laterRoundRules[i], initialIdbFacts[i]));
# 		}
# 	}
#
# 	@Override
# 	public synchronized IndexableFactCollection eval() {
# 		for (StratumEvaluator se : stratumEvals) {
# 			se.eval();
# 		}
# 		return allFacts;
# 	}
#
# 	private class StratumEvaluator {
# 		private ConcurrentFactIndexer<Set<PositiveAtom>> idbsPrev = FactIndexerFactory
# 				.createConcurrentSetFactIndexer();
# 		private ConcurrentFactIndexer<Set<PositiveAtom>> deltaOld = FactIndexerFactory
# 				.createConcurrentSetFactIndexer();
# 		private ConcurrentFactIndexer<Set<PositiveAtom>> deltaNew = FactIndexerFactory
# 				.createConcurrentSetFactIndexer();
# 		private final Map<PredicateSym, Set<ClauseEvaluator>> firstRoundEvals;
# 		private final Map<PredicateSym, Set<ClauseEvaluator>> laterRoundEvals;
# 		private final Set<PositiveAtom> initialIdbFacts;
#
# 		public StratumEvaluator(Map<PredicateSym, Set<SemiNaiveClause>> firstRoundRules,
# 				Map<PredicateSym, Set<SemiNaiveClause>> laterRoundRules, Set<PositiveAtom> initialIdbFacts) {
# 			Function<Map<PredicateSym, Set<SemiNaiveClause>>, Map<PredicateSym, Set<ClauseEvaluator>>> translate = (
# 					clauseMap) -> {
# 				Map<PredicateSym, Set<ClauseEvaluator>> evalMap = new HashMap<>();
# 				for (Map.Entry<PredicateSym, Set<SemiNaiveClause>> entry : clauseMap.entrySet()) {
# 					Set<ClauseEvaluator> s = new HashSet<>();
# 					for (SemiNaiveClause cl : entry.getValue()) {
# 						s.add(new ClauseEvaluator(cl, this::addFact, this::getFacts));
# 					}
# 					evalMap.put(entry.getKey(), s);
# 				}
# 				return evalMap;
# 			};
# 			firstRoundEvals = translate.apply(firstRoundRules);
# 			laterRoundEvals = translate.apply(laterRoundRules);
# 			this.initialIdbFacts = initialIdbFacts;
# 		}
#
# 		public void eval() {
# 			deltaNew.addAll(this.initialIdbFacts);
# 			evalOneRound(allFacts, firstRoundEvals);
# 			while (evalOneRound(deltaOld, laterRoundEvals)) {
# 				// Loop...
# 			}
# 		}
#
# 		private boolean evalOneRound(FactIndexer index, Map<PredicateSym, Set<ClauseEvaluator>> rules) {
# 			for (PredicateSym pred : index.getPreds()) {
# 				Set<ClauseEvaluator> evals = rules.get(pred);
# 				if (evals != null) {
# 					for (ClauseEvaluator eval : evals) {
# 						for (PositiveAtom fact : index.indexInto(pred)) {
# 							eval.evaluate(fact);
# 						}
# 					}
# 				}
# 			}
#
# 			if (deltaNew.isEmpty()) {
# 				return false;
# 			}
#
# 			idbsPrev.addAll(deltaOld);
# 			allFacts.addAll(deltaNew);
# 			deltaOld = deltaNew;
# 			deltaNew = FactIndexerFactory.createConcurrentSetFactIndexer();
# 			return true;
# 		}
#
# 		private boolean addFact(PositiveAtom fact, ClauseSubstitution subst) {
# 			fact = fact.applySubst(subst);
# 			Set<PositiveAtom> set = allFacts.indexInto(fact);
# 			if (!set.contains(fact)) {
# 				deltaNew.add(fact);
# 				return true;
# 			}
# 			return false;
# 		}
#
# 		private Iterable<PositiveAtom> getFacts(AnnotatedAtom atom, ClauseSubstitution subst) {
# 			Set<PositiveAtom> r = null;
# 			PositiveAtom unannotated = atom.asUnannotatedAtom();
# 			switch (atom.getAnnotation()) {
# 			case EDB:
# 				// Fall through...
# 			case IDB:
# 				r = allFacts.indexInto(unannotated, subst);
# 				break;
# 			case IDB_PREV:
# 				r = idbsPrev.indexInto(unannotated, subst);
# 				break;
# 			case DELTA:
# 				r = deltaOld.indexInto(unannotated, subst);
# 				break;
# 			default:
# 				assert false;
# 			}
# 			return r;
# 		}
# 	}
#
# }
