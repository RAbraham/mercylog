from typing import *
from pprint import pprint
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
from mercylog.abcdatalog.ast.validation.stratified_negation_validator import (
    StratifiedNegationValidator,
)
from mercylog.abcdatalog.ast.validation.stratified_program import StratifiedProgram
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.ast.visitors.head_visitor import HeadVisitor
from mercylog.abcdatalog.ast.visitors.premise_visitor import PremiseVisitor
from mercylog.abcdatalog.ast.visitors.premise_visitor_builder import (
    PremiseVisitorBuilder,
)
from mercylog.abcdatalog.engine.bottomup.annotated_atom import AnnotatedAtom
from mercylog.abcdatalog.engine.bottomup.clause_evaluator import ClauseEvaluator
from mercylog.abcdatalog.engine.bottomup.eval_manager import EvalManager
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import (
    SemiNaiveClauseAnnotator,
)
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import (
    SemiNaiveClause,
)
from mercylog.abcdatalog.util.utilities import Utilities
from mercylog.abcdatalog.util.datastructures.concurrent_fact_indexer import (
    ConcurrentFactIndexer,
)
from mercylog.abcdatalog.util.datastructures.fact_indexer import FactIndexer
from mercylog.abcdatalog.util.datastructures.fact_indexer_factory import (
    FactIndexerFactory,
)
from mercylog.abcdatalog.util.datastructures.indexable_fact_collection import (
    IndexableFactCollection,
)
from mercylog.abcdatalog.util.substitution.clause_substitution import ClauseSubstitution
from mercylog.abcdatalog.engine.bottomup.annotated_atom import Annotation


class StratumEvaluator:
    def __init__(
        self,
        first_round_rules: Dict[PredicateSym, Set[SemiNaiveClause]],
        later_round_rules: Dict[PredicateSym, Set[SemiNaiveClause]],
        initial_idb_facts,
        all_facts,
    ):
        def translate(clause_map):
            eval_map: Dict[PredicateSym, Set[ClauseEvaluator]] = dict()
            entry: Tuple[PredicateSym, Set[SemiNaiveClause]]
            for entry in clause_map.items():
                s: Set[ClauseEvaluator] = set()
                cl: SemiNaiveClause
                for cl in entry[1]:
                    s.add(ClauseEvaluator(cl, self.add_fact, self.get_facts))
                eval_map[entry[0]] = s
            return eval_map

        self.firstRoundEvals = translate(first_round_rules)
        self.laterRoundEvals = translate(later_round_rules)
        self.initialIdbFacts: Set[PositiveAtom] = initial_idb_facts
        self.deltaNew: ConcurrentFactIndexer = (
            FactIndexerFactory.createConcurrentSetFactIndexer()
        )
        self.deltaOld: ConcurrentFactIndexer = (
            FactIndexerFactory.createConcurrentSetFactIndexer()
        )
        self.idbsPrev: ConcurrentFactIndexer = (
            FactIndexerFactory.createConcurrentSetFactIndexer()
        )
        self.allFacts: ConcurrentFactIndexer = all_facts

    def eval(self):
        self.deltaNew.addAll_facts(self.initialIdbFacts)
        self.eval_one_round(self.allFacts, self.firstRoundEvals)
        while self.eval_one_round(self.deltaOld, self.laterRoundEvals):
            pass

    def eval_one_round(
        self, index: FactIndexer, rules: Dict[PredicateSym, Set[ClauseEvaluator]]
    ) -> bool:
        for pred in index.getPreds():
            evals: Set[ClauseEvaluator] = rules.get(pred)
            if evals is not None:
                eval: ClauseEvaluator
                for eval in evals:
                    for fact in index.indexInto_predsym(pred):
                        eval.evaluate(fact)
                pass
        if self.deltaNew.isEmpty():
            return False

        self.idbsPrev.addAll_indexable_fact_collection(self.deltaOld)
        self.allFacts.addAll_indexable_fact_collection(self.deltaNew)
        self.deltaOld = self.deltaNew
        self.deltaNew = FactIndexerFactory.createConcurrentSetFactIndexer()
        return True

    # def add_fact(self, fact: PositiveAtom, subst: ClauseSubstitution) -> bool:
    #     fact = fact.applySubst(subst)
    #     a_set: Set[PositiveAtom] = self.allFacts.indexInto_patom(fact)
    #     if fact not in a_set:
    #         self.deltaNew.add(fact)
    #         return True
    #     return False
    def add_fact(self, fact: PositiveAtom, subst: ClauseSubstitution) -> None:
        fact = fact.applySubst(subst)
        a_set: Set[PositiveAtom] = self.allFacts.indexInto_patom(fact)
        if fact not in a_set:
            self.deltaNew.add(fact)

    def get_facts(
        self, atom: AnnotatedAtom, subst: ClauseSubstitution
    ) -> Iterable[PositiveAtom]:
        r: Optional[Set[PositiveAtom]] = None
        unannotated: PositiveAtom = atom.asUnannotatedAtom()
        annotation = atom.getAnnotation()
        if annotation == Annotation.IDB or annotation == Annotation.EDB:
            r = self.allFacts.indexInto_patom_with_substitution(unannotated, subst)
        elif annotation == Annotation.IDB_PREV:
            r = self.idbsPrev.indexInto_patom_with_substitution(unannotated, subst)
        elif annotation == Annotation.DELTA:
            r = self.deltaOld.indexInto_patom_with_substitution(unannotated, subst)
        return r


class LocalHeadVisitor(HeadVisitor):
    def __init__(self):
        super(LocalHeadVisitor, self).__init__()

    def visit(self, atom: PositiveAtom, state) -> PredicateSym:
        return atom.getPred()


class SemiNaiveEvalManager(EvalManager):
    def __init__(self):
        self.allFacts: ConcurrentFactIndexer = (
            FactIndexerFactory.createConcurrentSetFactIndexer()
        )
        self.stratumEvals: List[StratumEvaluator] = []
        super(SemiNaiveEvalManager, self).__init__()

    def initialize(self, program: Set[Clause]):
        prog: UnstratifiedProgram = (
            DatalogValidator()
            .withBinaryDisunificationInRuleBody()
            .withBinaryUnificationInRuleBody()
            .withAtomNegationInRuleBody()
            .validate(program)
        )
        stratified_program: StratifiedProgram = StratifiedNegationValidator.validate(
            prog
        )

        # E.g.strata. [{node}, {tc}, {not_tc}]
        strata: List[Set[PredicateSym]] = stratified_program.getStrata()

        strata_number = len(strata)
        first_round_rules: List[Dict[PredicateSym, Set[SemiNaiveClause]]] = []
        later_round_rules: List[Dict[PredicateSym, Set[SemiNaiveClause]]] = []
        self.initial_idb_facts: List[Set[PositiveAtom]] = []
        for i in range(strata_number):
            first_round_rules.append(dict())
            later_round_rules.append(dict())
            self.initial_idb_facts.append(set())

        # E.g. for pred_to_stratum_map. {not_tc: 2, node: 1, tc: 0}
        pred_to_stratum_map: Dict[
            PredicateSym, int
        ] = stratified_program.getPredToStratumMap()

        for clause in prog.getRules():
            pred: PredicateSym = get_head_predicate(clause)
            stratum: int = pred_to_stratum_map.get(pred)
            #  Treat IDB predicates from earlier strata as EDB predicates.
            idbs: Set[PredicateSym] = strata[stratum]

            annotator: SemiNaiveClauseAnnotator = SemiNaiveClauseAnnotator(list(idbs))
            has_idb_pred = False
            c: Premise
            for c in clause.getBody():
                has_idb_pred = clause_has_idb_pred(c, idbs, has_idb_pred)

            rule: SemiNaiveClause
            for rule in annotator.annotate_single(clause):
                body_pred: PredicateSym = rule.getFirstAtom().getPred()
                if has_idb_pred:
                    Utilities.getSetFromMap(later_round_rules[stratum], body_pred).add(
                        rule
                    )
                else:
                    Utilities.getSetFromMap(first_round_rules[stratum], body_pred).add(
                        rule
                    )

        edbs: Set[PredicateSym] = prog.getEdbPredicateSyms()
        fact: PositiveAtom
        for fact in prog.getInitialFacts():
            if fact.getPred() in edbs:
                self.allFacts.add(fact)
            else:
                self.initial_idb_facts[pred_to_stratum_map.get(fact.getPred())].add(
                    fact
                )

        for i in range(strata_number):
            self.stratumEvals.append(
                StratumEvaluator(
                    first_round_rules[i],
                    later_round_rules[i],
                    self.initial_idb_facts[i],
                    self.allFacts,
                )
            )

    def eval(self) -> IndexableFactCollection:
        se: StratumEvaluator
        for se in self.stratumEvals:
            se.eval()
        return self.allFacts


def clause_has_idb_pred(c, idbs, has_idb_pred):
    # aaa. Simplify this next
    patom_func = lambda atom, idb: atom.getPred() in idbs or idb
    check_for_idb_pred: PremiseVisitor[bool, bool] = (
        PremiseVisitorBuilder().onPositiveAtom(patom_func).or_(lambda premise, idb: idb)
    )
    return c.accept_premise_visitor(check_for_idb_pred, has_idb_pred)


def get_head_predicate(clause: Clause):
    # OLD AbcDatalog code: Start
    # get_head_pred: HeadVisitor = LocalHeadVisitor()
    # return clause.getHead().accept_head_visitor(get_head_pred, None)
    # OLD AbcDatalog code: End
    return clause.getHead().getPred()
