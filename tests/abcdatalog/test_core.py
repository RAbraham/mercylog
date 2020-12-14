from typing import *
import toolz

from mercylog.abcdatalog.ast.validation.datalog_validation_exception import (
    DatalogValidationException,
)

from mercylog.types import relation, variables, _
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import q as do_query
import pytest

from tests.abcdatalog.helper import initEngine_engine, seminaive_engine
from functools import partial

p = relation("p")
q = relation("q")
r = relation("r")
s = relation("s")

V, W, X, Y, Z = variables("V", "W", "X", "Y", "Z")


@toolz.curry
def is_result(engine, a_query, exp_result):
    rs = do_query(engine, a_query)
    return _equals(rs, exp_result)


def list_set(a_list: List) -> List:
    result = []
    for a in a_list:
        if a not in result:
            result.append(a)
    return result


def _equals(act, exp):
    _act = list_set(act)
    _exp = list_set(exp)

    assert len(_act) == len(_exp), f"Act:{act} is not of same size as Exp:{exp}"
    for e in _exp:
        assert e in _act, f"Fact:{e} was not present in Actual:{act}"
    return True


@toolz.curry
def match(program, query, result):
    semi_engine = seminaive_engine()
    initEngine = partial(initEngine_engine, semi_engine)
    engine = initEngine(program)
    return is_result(engine, query, result)


def test_queryUndefinedPredicate():
    program = [p()]
    ans = match(program)
    assert ans(q(), [])


def test_queryEDBPredicate():
    a_q1 = q("a", "b", "c", "d", "e")
    a_q2 = q("e", "d", "c", "b", "a")
    program = [p(), a_q1, a_q2]
    ans = match(program)
    assert ans(p(), [p()])
    assert ans(q(V, W, X, Y, Z), [a_q1, a_q2])
    assert ans(q(W, "b", X, Y, Z), [a_q1])
    assert ans(q(W, X, "d", Y, Z), [])


def test_queryNonRecursiveIDBPredicate():
    program = [
        p("a", "b"),
        p("b", "c"),
        p("c", "d"),
        q(X, Y) <= [p(X, Z), p(Z, Y)],
    ]
    ans = match(program)
    assert ans(q(X, Y), [q("a", "c"), q("b", "d")])
    assert ans(q(X, "c"), [q("a", "c")])
    assert ans(q("x", "b"), [])


def test_queryLinearlyRecursiveIDBPredicate():
    # 		// Acyclic transitive closure.
    program = [
        p("a", "b"),
        p("b", "c"),
        p("c", "d"),
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [p(X, Z), q(Z, Y)],
    ]
    ans = match(program)
    assert ans(
        q(X, Y),
        [q("a", "b"), q("a", "c"), q("a", "d"), q("b", "c"), q("b", "d"), q("c", "d")],
    )

    assert ans(q("a", X), [q("a", "b"), q("a", "c"), q("a", "d")])


def test_transitive_closure_with_a_cycle():
    # 		// Transitive closure with a cycle.

    program = [
        p("a", "b"),
        p("b", "c"),
        p("c", "d"),
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [p(X, Z), q(Z, Y)],
        p("d", "c"),
    ]
    ans = match(program)
    assert ans(
        q(X, Y),
        [
            q("a", "b"),
            q("a", "c"),
            q("a", "d"),
            q("b", "c"),
            q("b", "d"),
            q("c", "c"),
            q("c", "d"),
            q("d", "c"),
            q("d", "d"),
        ],
    )


def test_queryNonLinearlyRecursiveIDBPredicate():
    program = [
        p("a", "b"),
        p("b", "c"),
        p("c", "d"),
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [q(X, Z), q(Z, Y)],
    ]

    ans = match(program)
    assert ans(
        q(X, Y),
        [q("a", "b"), q("a", "c"), q("a", "d"), q("b", "c"), q("b", "d"), q("c", "d")],
    )

    assert ans(q("a", X), [q("a", "b"), q("a", "c"), q("a", "d")])


def test_queryNonLinearlyRecursiveIDBPredicate_withCycle():
    #     // Transitive closure with a cycle.
    program = [
        p("a", "b"),
        p("b", "c"),
        p("c", "d"),
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [q(X, Z), q(Z, Y)],
        p("d", "c"),
    ]
    ans = match(program)
    assert ans(
        q(X, Y),
        [
            q("a", "b"),
            q("a", "c"),
            q("a", "d"),
            q("b", "c"),
            q("b", "d"),
            q("c", "c"),
            q("c", "d"),
            q("d", "c"),
            q("d", "d"),
        ],
    )


def test_queryIDBPredicateWithUndefinedEDB():
    program = [q(X, Y) <= p(X, Y), r("a", "b")]
    ans = match(program)
    assert ans(q(X, Y), [])


def test_queryIDBPredicateWithExplicitIDBFact():
    # // Note that q is defined by a rule, but we also give an explicit fact.
    program = [q(X, Y) <= r(X, Y), r("a", "b"), q("b", "c")]
    ans = match(program)
    assert ans(q(X, Y), [q("a", "b"), q("b", "c")])


def test_queryZeroAryPredicates():
    program = [p() <= q(), r() <= [p(), s()], q(), s()]
    ans = match(program)
    assert ans(q(), [q()])
    assert ans(p(), [p()])
    assert ans(s(), [s()])
    assert ans(r(), [r()])


def test_querymutuallyrecursivepredicates():
    program = [
        p(X, Y, Z) <= q(X, Y, Z),
        q(X, Y, Z) <= p(Z, Y, X),
        p(X, Y, Z) <= r(X, Y, Z),
        r("a", "b", "c"),
    ]

    ans = match(program)
    assert ans(p(X, Y, Z), [p("a", "b", "c"), p("c", "b", "a")])
    assert ans(p(X, "b", Y), [p("a", "b", "c"), p("c", "b", "a")])
    assert ans(p("a", X, "c"), [p("a", "b", "c")])
    assert ans(p(X, "c", Y), [])


def test_querymutuallyrecursivepredicates_no_facts():
    program = [p(X, Y, Z) <= q(X, Y, Z), q(X, Y, Z) <= p(X, Y, Z)]
    ans = match(program)
    assert ans(p(X, Y, Z), [])
    assert ans(q(X, Y, Z), [])


def test_queryNestedPredicates():
    one = relation("1")
    two = relation("2")
    three = relation("3")
    four = relation("4")
    five = relation("5")
    program = [
        one(X, Y, Z) <= two(X, Y, Z),
        two(X, Y, Z) <= three(X, Y, Z),
        three(X, Y, Z) <= four(X, Y, Z),
        four(X, Y, Z) <= five(X, Y, Z),
        five("a", "b", "c"),
    ]

    assert match(program, one(X, Y, Z), [one("a", "b", "c")])


def test_queryIDBPredicatesWithConstants():
    program = [p("a", X) <= q(X, X), q("a", "a"), q("b", "b"), q("c", "d")]

    ans = match(program)
    assert ans(p(Z, W), [p("a", "a"), p("a", "b")])
    assert ans(p("a", X), [p("a", "a"), p("a", "b")])

    program = [p(X, X) <= q(X, "a"), q("a", "a"), q("b", "b"), q("c", "d")]
    ans = match(program)
    assert ans(p("a", X), [p("a", "a")])
    assert ans(p(X, "a"), [p("a", "a")])


#
# 	/**
# 	 * This test is primarily for exercising a corner case for engines that use
# 	 * a RuleBasedSubstitution. In this test case the rules do not have any
# 	 * variables, so various data structures in the substitution are empty.
# 	 */
def test_testRulesWithNoVariables():
    program = [p() <= q("a", "b"), q("a", "b")]
    ans = match(program)
    assert ans(p(), [p()])

    program = [p() <= [q("a", "b"), r("c", "d")], q("a", "b"), r("c", "d")]
    ans = match(program)
    assert ans(p(), [p()])


# 	}
#
# 	/**
# 	 * This test is primarily for exercising a corner case for engines that use
# 	 * a RuleBasedSubstitution. We want to make sure that even though a
# 	 * substitution might be completely computed (i.e., every variable in the
# 	 * rule has an acceptable mapping), the rest of the rule is also correctly
# 	 * processed.
# 	 */
def test_testRuleThatEndsInAGroundAtom():

    edge = relation("edge")
    tc = relation(("tc"))
    trigger = relation("trigger")
    program = [
        edge(0, 1),
        edge(1, 2),
        edge(2, 3),
        tc(X, Y) <= edge(X, Y),
        tc(X, Y) <= [edge(X, Z), tc(Z, Y), trigger()],
    ]

    ans = match(program)
    assert ans(tc(X, Y), [tc(0, 1), tc(1, 2), tc(2, 3)])

    program = program + [trigger()]
    ans = match(program)
    assert ans(tc(X, Y), [tc(0, 1), tc(0, 2), tc(0, 3), tc(1, 2), tc(1, 3), tc(2, 3)])


#
# 	/**
# 	 * This test is primarily for exercising a corner case for engines that use
# 	 * a RuleBasedSubstitution. We want to make sure that variables are
# 	 * consistently bound while an individual atom is being processed.
# 	 */
def test_testRulesWithRepeatedVariablesInAnAtom():
    program = [
        p(X) <= q(X, X),
        q("a", "a"),
        q("a", "b"),
        q("b", "b"),
    ]
    ans = match(program)
    assert ans(p(X), [p("a"), p("b")])
    program = [
        p(X, Y) <= q(Y, X, Y, X),
        q("a", "a", "a", "a"),
        q("a", "a", "a", "b"),
        q("a", "a", "b", "b"),
        q("a", "b", "b", "b"),
        q("b", "b", "b", "b"),
    ]

    ans = match(program)

    assert ans(p(X, Y), [p("a", "a"), p("b", "b")])


def test_testRulesWithLongBodies():
    a = relation("a")
    b = relation("b")
    c = relation("c")
    d = relation("d")
    e = relation("e")
    f = relation("f")
    g = relation("g")
    A, B, C, D, E, F, G = variables("A", "B", "C", "D", "E", "F", "G")
    X = variables(*["X" + str(r) for r in range(1, 23)])

    program = [
        p(A, B, C, D, E, F, G) <= [a(A), b(B), c(C), d(D), e(E), f(F), g(G)],
        a(1),
        b(1),
        c(1),
        d(1),
        d(2),
        e(1),
        f(1),
        g(1),
    ]

    ans = match(program)
    assert ans(p(A, B, C, D, E, F, G), [p(1, 1, 1, 1, 1, 1, 1), p(1, 1, 1, 2, 1, 1, 1)])

    foo1 = "foo1"
    foo2 = "foo2"
    foo3 = "foo3"
    foo4 = "foo4"
    foo5 = "foo5"
    bar = "bar"
    program = [
        p(A, B, C, D, E)
        <= [
            a(A, X[1], X[2], X[3], X[5]),
            b(X[6], B, X[7], X[8], X[9]),
            c(X[10], X[11], C, X[12], X[13]),
            d(X[14], X[15], X[16], D, X[17]),
            e(X[18], X[19], X[20], X[21], E),
        ],
        a(foo1, 2, 3, 4, 5),
        b(6, foo2, 8, 9, 10),
        c(11, 12, foo3, 14, 15),
        d(16, 17, 18, foo4, 20),
        e(21, 22, 23, 24, foo5),
        c(foo1, foo2, bar, foo4, foo5),
    ]
    ans = match(program)
    assert ans(
        p(A, B, C, D, E),
        [p(foo1, foo2, foo3, foo4, foo5), p(foo1, foo2, bar, foo4, foo5)],
    )


def test_testRulesWithUnusedVariables1():
    or_ = relation("or")
    on = relation("on")
    L, L1 = variables("L", "L1")
    a = "a"
    b = "b"
    c = "c"
    program = [on(L) <= [or_(L, L1, X), on(L1)], or_(a, b, c), on(b)]
    ans = match(program)
    assert ans(on(a), [on(a)])
    assert ans(on(X), [on(a), on(b)])


def test_testRulesWithUnusedVariables2():
    or_ = relation("or")
    on = relation("on")
    L, L1 = variables("L", "L1")
    a = "a"
    b = "b"
    c = "c"
    program = [
        on(L) <= [or_(L, L1, X), on(L1)],
        on(L) <= [or_(L, X, L1), on(L1)],
        or_(a, b, c),
        on(b),
    ]

    ans = match(program)
    assert ans(on(a), [on(a)])
    assert ans(on(X), [on(a), on(b)])


def testRulesWithAnonymousVariables():
    or_ = relation("or")
    on = relation("on")
    L, L1 = variables("L", "L1")
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    program = [
        on(L) <= [or_(L, L1, _), on(L1)],
        on(L) <= [or_(L, _, L1), on(L1)],
        or_(a, b, c),
        on(b),
    ]
    ans = match(program)
    assert ans(on(a), [on(a)])
    assert ans(on(_), [on(a), on(b)])
    program = [p() <= [q(_, _), r(_, _)], q(a, b), r(c, d)]
    ans = match(program)
    assert ans(p(), [p()])

def test_testUnboundVariable1():
    a = "a"
    b = "b"
    with pytest.raises(DatalogValidationException):
        match([p(X, b)], p(X, Y), [])
        match([q(X,Y) <= p(X,b), p(a,b)], q(X,Y), [])

def test_testRulesWithTrue():
    a = "a"
    true = relation("true")
    false = relation("false")

    assert match([false()], true(), [])
    assert match([p(X) <= q(X), q(a)], true(), [])


def testEmptyProgram():
    anything = relation("anything")
    assert match([], anything(), [])