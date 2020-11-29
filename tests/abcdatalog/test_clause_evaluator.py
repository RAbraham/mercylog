import pytest
from typing import *
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.ast.binary_disunifier import BinaryDisunifier
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

    def verify(body: List[Premise]):
        cl = Clause(pXW, tuple(body))
        prog: UnstratifiedProgram = DatalogValidator().withBinaryUnificationInRuleBody().withBinaryDisunificationInRuleBody().validate({cl})
        annotator = SemiNaiveClauseAnnotator(list(prog.getIdbPredicateSyms()))
        it = iter(prog.getRules())
        rule = next(it)
        annotated = annotator.annotate_single(rule)
        it_annotated = iter(annotated)
        ordered = next(it_annotated)
        def facts_func_result(fact, s, result):
            r = fact.applySubst(s)
            result.append(r)

        from functools import partial
        result = []
        facts_func = partial(facts_func_result, result=result)
        eval = ClauseEvaluator(ordered, facts_func, lambda atom, s: facts)

        eval.evaluate(qab)
        return result

    assert verify([qXY, qZW]) == [PositiveAtom.create(p,[a, b]), PositiveAtom.create(p, [a, a])]
    assert verify([qXY, qYW]) == [PositiveAtom.create(p, [a, a])]
    uZY = BinaryUnifier(z, y)
    assert verify([qXY, qZW, uZY]) == [PositiveAtom.create(p, [a, a])]
    uXZ = BinaryUnifier(x, z)
    assert verify([qXY, qZW, uXZ]) == [PositiveAtom.create(p, [a, b])]
    uXY = BinaryUnifier(x, y)
    assert verify([qXY, qZW, uXY]) == []

    dZY = BinaryDisunifier(z, y)
    assert verify([qXY, qZW, dZY]) == [PositiveAtom.create(p, [a, b])]
    dWY = BinaryDisunifier(w, y)
    assert verify([qXY, qZW, dWY]) == [PositiveAtom.create(p, [a, a])]