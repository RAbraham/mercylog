import pytest
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClauseAnnotator

def test_error():
    x = Variable.create("X")
    y = Variable.create("Y")
    z = Variable.create("Z")
    w = Variable.create("W")
    p = PredicateSym.create("p", 2)
    q = PredicateSym.create("q", 2)
    qXY = PositiveAtom.create(q, [x, y])
    pXW = PositiveAtom.create(p, [x, w])
    qZW = PositiveAtom.create(q, [z, w])
    body = [qXY, qZW]

    cl = Clause(pXW, tuple(body))
    prog: UnstratifiedProgram = DatalogValidator().withBinaryUnificationInRuleBody().withBinaryDisunificationInRuleBody().validate(
        {cl})
    annotator = SemiNaiveClauseAnnotator(list(prog.getIdbPredicateSyms()))
    it = iter(prog.getRules())
    rule = next(it)
    annotated = annotator.annotate_single(rule)
    assert str(annotated) == "[p(X, W) :- q(X, Y)<EDB>, q(Z, W)<EDB>.]"



