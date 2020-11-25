import pytest
from typing import *
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator, DatalogValidationException
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClauseAnnotator
from mercylog.abcdatalog.engine.bottomup.clause_evaluator import ClauseEvaluator


def test_clause_evaluator():
    a = Constant.create("a")
    b = Constant.create("b")
    x = Variable.create("X")
    y = Variable.create("Y")
    z = Variable.create("Z")
    w = Variable.create("W")
    p = PredicateSym.create("p", 2)
    q = PredicateSym.create("q", 2)
    qab = PositiveAtom.create(q, [a, b])
    qba = PositiveAtom.create(q, [b, a])
    facts = [qab, qba]
    qXY = PositiveAtom.create(q, [x, y])
    qZW = PositiveAtom.create(q, [z, w])
    qYW = PositiveAtom.create(q, [y, w])
    pXW = PositiveAtom.create(p, [x, w])

    def test(body: List[Premise]):
#     System.out.print("\nTesting: ");
        print("\n Testing")
#     Clause cl = new Clause(pXW, body);
        cl = Clause(pXW, tuple(body))
#     UnstratifiedProgram prog = null;
        prog: UnstratifiedProgram = DatalogValidator().withBinaryUnificationInRuleBody().withBinaryDisunificationInRuleBody().validate({cl})
#     SemiNaiveClauseAnnotator annotator = new SemiNaiveClauseAnnotator(prog.getIdbPredicateSyms());
        annotator = SemiNaiveClauseAnnotator(list(prog.getIdbPredicateSyms()))
#     SemiNaiveClause ordered = annotator.annotate(prog.getRules().iterator().next()).iterator().next();
        it = iter(prog.getRules())
        rule = next(it)
        annotated = annotator.annotate_single(rule)
        it_annotated = iter(annotated)
        ordered = next(it_annotated)
#     System.out.println(ordered);
        print(ordered)
#     ClauseEvaluator eval = new ClauseEvaluator(ordered, (fact, s) -> System.out.println(fact.applySubst(s)),
#             (atom, s) -> facts);
        def facts_func(fact, s):
            print(fact.applySubst(s))

        eval = ClauseEvaluator(ordered, facts_func, lambda atom, s: facts)

        #     eval.evaluate(qab);
        eval.evaluate(qab)

    # test.accept(Arrays.asList(qXY, qZW));
    test([qXY, qZW])
    # test.accept(Arrays.asList(qXY, qYW));
    # BinaryUnifier uZY = new BinaryUnifier(z, y);
    # test.accept(Arrays.asList(qXY, qZW, uZY));
    # BinaryUnifier uXZ = new BinaryUnifier(x, z);
    # test.accept(Arrays.asList(qXY, qZW, uXZ));
    # BinaryUnifier uXY = new BinaryUnifier(x, y);
    # test.accept(Arrays.asList(qXY, qZW, uXY));
    # BinaryDisunifier dZY = new BinaryDisunifier(z, y);
    # test.accept(Arrays.asList(qXY, qZW, dZY));
    # BinaryDisunifier dWY = new BinaryDisunifier(w, y);
	# test.accept(Arrays.asList(qXY, qZW, dWY));
    pass