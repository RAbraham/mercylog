import pytest
from mercylog.abcdatalog.ast.predicate_sym import PredicateSym
from mercylog.abcdatalog.ast.variable import Variable
from mercylog.abcdatalog.ast.constant import Constant
from mercylog.abcdatalog.ast.head import Head
from mercylog.abcdatalog.ast.clause import Clause
from mercylog.abcdatalog.ast.positive_atom import PositiveAtom
from mercylog.abcdatalog.ast.premise import Premise
from mercylog.abcdatalog.ast.binary_unifier import BinaryUnifier
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClause
from mercylog.abcdatalog.util.substitution.clause_substitution import ClauseSubstitution
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.engine.bottomup.semi_naive_clause_annotator import SemiNaiveClauseAnnotator
from mercylog.abcdatalog.ast.validation.datalog_validator import ValidClause
from typing import *

def test_create_substitution_1():
    p0 = PredicateSym.create("p", 0)
    q2 = PredicateSym.create("q", 2)
    r2 = PredicateSym.create("r", 2)
    s3 = PredicateSym.create("s", 3)
    x: Variable
    y: Variable
    z: Variable
    x = Variable.create("X")
    y = Variable.create("Y")
    z = Variable.create("Z")
    a: Constant
    b: Constant
    a = Constant.create("a")
    b = Constant.create("b")
    idbPreds: List = [q2, s3]
    pAtom = PositiveAtom.create(p0, [])
    qAtom: Premise = PositiveAtom.create(q2, [x, y])
    rAtom: Premise = PositiveAtom.create(r2, [x, x])
    sAtom: Premise = PositiveAtom.create(s3, [a, x, z])
    u1: Premise = BinaryUnifier(x, b)
    u2: Premise = BinaryUnifier(z, z)
    validator: DatalogValidator = DatalogValidator().withBinaryUnificationInRuleBody()


    annotator: SemiNaiveClauseAnnotator = SemiNaiveClauseAnnotator(idbPreds)
    expected_value = "{ }"
    input_clause = {Clause(pAtom, tuple([pAtom]))} #ignore

    assert_annotation(validator, annotator, input_clause, expected_value)
    assert_annotation(validator, annotator, {Clause(pAtom, tuple([qAtom]))}, "{ ^ <0> X -> None, Y -> None }")
    l: List[Premise] = [qAtom, rAtom]

    assert_annotation(validator, annotator, {Clause(pAtom, tuple(l))}, "{ ^ <0> X -> None, Y -> None }")
    l[0], l[1] = l[1], l[0]

    assert_annotation(validator, annotator, [Clause(pAtom, tuple(l))], "{ ^ <0> X -> None, Y -> None }")
    l = [qAtom, sAtom]
    subst = clause_substitution(annotator, [Clause(pAtom, tuple(l))], validator)
    assert str(subst) == "{ ^ <0> X -> None, Y -> None, <1> Z -> None }"

    subst.add(x, a)

    assert str(subst) == "{ <0> X -> a, ^ Y -> None, <1> Z -> None }"

    with pytest.raises(AssertionError): #Correctly threw error when adding in wrong order"
        subst.add(z, a)
    subst.add(y, b)
    assert str(subst) == "{ <0> X -> a, Y -> b, ^ <1> Z -> None }"
    with pytest.raises(AssertionError): # Correctly threw error when adding in wrong order
        subst.add(x, a)
    subst.add(z, a)
    assert str(subst) == "{ <0> X -> a, Y -> b, <1> Z -> a }"
    with pytest.raises(AssertionError): # Correctly threw error when adding a variable not in substitution
        subst.add(Variable.create("w"), b)
    subst.resetState(0)
    assert not subst.get(x)
    subst.add(x, a)
    assert subst.get(x) == a
    subst.add(y, b)

    assert subst.get(x) == a
    assert subst.get(y) == b
    subst.add(z, a)
    assert subst.get(x) == a
    assert subst.get(y) == b
    assert subst.get(z) == a
    subst.resetState(1)
    assert subst.get(x) == a
    assert subst.get(y) == b
    assert not subst.get(z)

def test_evaluation_error():
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
    print("\n>> annotated")
    print(annotated)
    it_annotated = iter(annotated)
    ordered = next(it_annotated)
    subst = ClauseSubstitution.make_with_seminaive_clause(ordered)
    assert subst.index == {z: 2, w: 3, x: 0, y: 1}
    assert str(subst) == "{ ^ <0> X -> None, Y -> None, <1> Z -> None, W -> None }"


def assert_annotation(validator, annotator, input_clause, expected_value):
    act_value = clause_substitution(annotator, input_clause, validator)
    assert str(act_value) == expected_value
    return annotator


def clause_substitution(annotator, input_clause, validator):
    rule = get_cl(validator, input_clause)
    _clause = list(annotator.annotate_single(rule))[0]
    subst = ClauseSubstitution.make_with_seminaive_clause(_clause)
    return subst


def get_cl(validator, input_clause):
    prog: UnstratifiedProgram = validator.validate(input_clause)  # ignore
    it = iter(prog.getRules())
    rule = next(it)
    return rule