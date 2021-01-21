import pytest
from mercylog.abcdatalog.ast.validation.datalog_validation_exception import (
    DatalogValidationException,
)


from mercylog.types import relation, _, eq, not_eq, gt

from tests.abcdatalog.helper import match_relations, X, Y, Z, p, q, parse, tc, edge, cycle, beginsNotAtC, beginsAtC, noncycle, noC, a, b, c, d, e



def test_testRulesWithBinaryUnifiers():

    program = [
        tc(X, Y) <= edge(X, Y),
        tc(X, Y) <= [edge(X, Z), tc(Z, Y)],
        edge(a, b),
        edge(b, c),
        edge(c, c),
        edge(c, d),
        cycle(X) <= [eq(X, Y), tc(X, Y)],
        beginsAtC(X, Y) <= [tc(X, Y), eq(c, X)],
    ]
    ans = match_relations(program)
    assert ans(cycle(X), [cycle(c)])
    assert ans(beginsAtC(X, Y), [beginsAtC(c, c), beginsAtC(c, d)])


def test_testRulesWithBinaryDisunifiers():
    program = [
        tc(X, Y) <= edge(X, Y),
        tc(X, Y) <= [edge(X, Z), tc(Z, Y)],
        edge(a, b),
        edge(b, c),
        edge(c, c),
        edge(c, d),
        noncycle(X, Y) <= [not_eq(X, Y), tc(X, Y)],
        beginsNotAtC(X, Y) <= [tc(X, Y), not_eq(c, X)],
        noC(X, Y) <= [edge(X, Y), not_eq(X, c), not_eq(Y, c)],
        noC(X, Y) <= [noC(X, Z), noC(Z, Y)],
    ]

    ans = match_relations(program)
    assert ans(
        noncycle(X, Y),
        [
            noncycle(a, b),
            noncycle(a, c),
            noncycle(a, d),
            noncycle(b, c),
            noncycle(b, d),
            noncycle(c, d),
        ],
    )
    assert ans(
        beginsNotAtC(X, Y),
        [
            beginsNotAtC(a, b),
            beginsNotAtC(a, c),
            beginsNotAtC(a, d),
            beginsNotAtC(b, c),
            beginsNotAtC(b, d),
        ],
    )
    assert ans(noC(X, Y), [noC(a, b)])


def test_testBinaryUnificationNoAtom():
    program = [
        p(X, b) <= eq(X, a),
        p(b, Y) <= eq(Y, a),
        p(X, Y) <= [eq(X, c), eq(Y, d)],
        p(X, X) <= eq(X, c),
        p(X, Y) <= [eq(X, d), eq(Y, X)],
        p(X, Y) <= [eq(X, Y), eq(X, e)],
    ]

    ans = match_relations(program)
    assert ans(p(X, Y), [p(a, b), p(b, a), p(c, d), p(c, c), p(d, d), p(e, e)])
    program = program + [q(X, Y) <= p(X, Y)]
    ans = match_relations(program)
    assert ans(q(X, Y), [q(a, b), q(b, a), q(c, d), q(c, c), q(d, d), q(e, e)])


def testUselessBinaryUnification():
    program = [p(X) <= [q(X), eq(X, Y)], q(a), p(b) <= eq(X, _)]
    ans = match_relations(program)
    with pytest.raises(DatalogValidationException):
        ans(p(X), [])


def testImpossibleBinaryUnification1():
    assert match_relations([p() <= eq(a, b)], p(), [])


# public void testImpossibleBinaryUnification2() throws DatalogValidationException {
def test_testImpossibleBinaryUnification2():
    assert match_relations([p() <= [eq(Z, b), eq(X, Y), eq(a, X), eq(Z, Y)]], p(), [])


def test_testBinaryDisunificationNoAtom():
    program = [p() <= not_eq(a, b), q() <= [not_eq(X, Y), eq(X, a), eq(Y, b)]]
    ans = match_relations(program)
    assert ans(p(), [p()])
    assert ans(q(), [q()])


def test_testImpossibleBinaryDisunification1():
    assert match_relations([p() <= not_eq(a, a)], p(), [])


def test_testImpossibleBinaryDisunification2():
    program = [p() <= [eq(Z, a), not_eq(X, Y), eq(a, X), eq(Z, Y)]]
    assert match_relations(program, p(), [])


def test_testImpossibleBinaryDisunification3():
    program = [p() <= [q(X), eq(X, X)]]
    ans = match_relations(program)
    assert ans(p(), [])


def test_testBinaryDisunificationFail1():
    program = [p() <= [~q(a, b), not_eq(X, _)]]
    with pytest.raises(DatalogValidationException):
        match_relations(program, p(), [])


def test_testBinaryDisunificationFail2():
    program = [p(X) <= [q(X), not_eq(Y, _)], q(a)]
    with pytest.raises(DatalogValidationException):
        match_relations(program, p(X), [])

# def test_gt():
#     age = relation("age")
#     senior = relation("senior")
#     program = [
#         age("John", 28),
#         age("Mary", 40),
#         age("Dad", 60),
#         age("Mom", 70),
#         senior(X, Y) <= [age(X, Y), gt(Y, 59)]
#     ]
#     ans = match_relations(program)
#     assert ans(senior(X, Y), [age("Dad", 60), age("Mom", 70)])