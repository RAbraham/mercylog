import unittest
import pytest
from mercylog.types import relation, Variable, _
from mercylog.abcdatalog.ast.validation.unstratified_program import UnstratifiedProgram
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidator
from mercylog.abcdatalog.ast.validation.stratified_negation_graph import StratifiedNegationGraph
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import convert
from mercylog.abcdatalog.ast.validation.datalog_validator import DatalogValidationException
from pprint import pprint

def test_reachable():
    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")
    reachable = relation("reachable")
    edge = relation("edge")
    not_reachable = relation("not_reachable")
    node = relation("node")

    program = [
        reachable(X, Y) <= edge(X, Y),
        reachable(X, Y) <= [edge(X, Z), reachable(Z, Y)],
        not_reachable(X, Y) <= [node(X), node(Y), ~reachable(X, Y)],
        node(X) <= edge(X, _),
        node(X) <= edge(_, X)
    ]
    abc_program = convert(program)

    sorted_strata_str = validate(abc_program)
    exp = ['{reachable}', '{node}', '{not_reachable}']
    assert sorted_strata_str[-1] == exp[-1]


def validate(abc_program):
    v: UnstratifiedProgram = DatalogValidator().withAtomNegationInRuleBody().validate(abc_program)
    g: StratifiedNegationGraph = StratifiedNegationGraph.create(v)
    sorted_strata_str = [str(s) for s in g.strata]
    return sorted_strata_str


def test_pq():
    p = relation("p")
    q = relation('q')
    r = relation('r')

    program = [
        p() <= [q(), ~r()],
        q() <= r(),
        r() <= q()
    ]
    abc_program = convert(program)
    strata_str = validate(abc_program)
    assert strata_str[-1] == '{p}'


def test_no_stratification():
    p = relation("p")
    q = relation("q")
    program = [
        p() <= ~q(),
        q() <= ~p()
    ]
    abc_program = convert(program)
    with pytest.raises(DatalogValidationException):
        validate(abc_program)

def test_simple():
    tc = relation("tc")
    edge = relation("edge")
    program = [
        tc() <= edge()
    ]
    abc_program = convert(program)
    strata_str = validate(abc_program)
    assert ['{tc}'] == strata_str


def test_simple_negated():
    p = relation("p")
    q = relation("q")
    program = [
        p() <= ~q()
    ]
    abc_program = convert(program)
    strata_str = validate(abc_program)
    assert strata_str == ['{p}']

    pass


if __name__ == '__main__':
    unittest.main()
