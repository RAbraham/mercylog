from mercylog.abcdatalog.ast.validation.datalog_validation_exception import (
    DatalogValidationException,
)
from mercylog.db import  facts
from mercylog.types import relation, variables, _
import pytest

from tests.abcdatalog.helper import (
    match_relations,
    match3,
    a,
    b,
    c,
    d,
    e,
    p,
    q,
    r,
    s,
    X,
    Y,
    Z,
    V,
    W,
)

# facts = db

def test_queryUndefinedPredicate():
    db1 = facts([p()])
    match3(db1, [], q(), [])


def test_queryEDBPredicate():
    a_q1 = q("a", "b", "c", "d", "e")
    a_q2 = q("e", "d", "c", "b", "a")
    db = [p(), a_q1, a_q2]
    assert match_relations(db, p(), [p()])

    ans = match3(facts(db), [])
    ans(q(V, W, X, Y, Z), [(a, b, c, d, e), (e, d, c, b, a)])
    ans(q(W, "b", X, Y, Z), [(a, c, d, e)])
    ans(q(W, X, "d", Y, Z), [])


def test_queryNonRecursiveIDBPredicate():
    db = facts([p("a", "b"), p("b", "c"), p("c", "d")])

    rules = [q(X, Y) <= [p(X, Z), p(Z, Y)]]
    ans = match3(db, rules)
    ans(q(X, Y), [(a, c), (b, d)])
    ans(q(X, c), [(a,)])
    ans(q("x", b), [])


def test_queryLinearlyRecursiveIDBPredicate():
    # 		// Acyclic transitive closure.
    db = facts(
        [
            p("a", "b"),
            p("b", "c"),
            p("c", "d"),
        ]
    )
    rules = [
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [p(X, Z), q(Z, Y)],
    ]
    ans = match3(db, rules)

    ans(q(X, Y), [(a, b), (a, c), (a, d), (b, c), (b, d), (c, d)])
    ans(q("a", X), [(b,), (c,), (d,)])



def test_transitive_closure_with_a_cycle():
    # 		// Transitive closure with a cycle.

    db = facts(
        [
            p("a", "b"),
            p("b", "c"),
            p("c", "d"),
            p("d", "c"),
        ]
    )
    rules = [q(X, Y) <= p(X, Y), q(X, Y) <= [p(X, Z), q(Z, Y)]]
    ans = match3(db, rules)
    ans(
        q(X, Y),
        [(a, b), (a, c), (a, d), (b, c), (b, d), (c, c), (c, d), (d, c), (d, d)],
    )


def test_queryNonLinearlyRecursiveIDBPredicate():
    db = facts(
        [
            p("a", "b"),
            p("b", "c"),
            p("c", "d"),
        ]
    )
    rules = [
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [q(X, Z), q(Z, Y)],
    ]

    ans = match3(db, rules)
    ans(q(X, Y), [(a, b), (a, c), (a, d), (b, c), (b, d), (c, d)])
    ans(q(a, X), [(b,), (c,), (d,)])


def test_queryNonLinearlyRecursiveIDBPredicate_withCycle():
    #     // Transitive closure with a cycle.
    db = facts(
        [
            p("a", "b"),
            p("b", "c"),
            p("c", "d"),
            p("d", "c"),
        ]
    )
    rules = [
        q(X, Y) <= p(X, Y),
        q(X, Y) <= [q(X, Z), q(Z, Y)],
    ]
    ans = match3(db, rules)
    ans(
        q(X, Y),
        [(a, b), (a, c), (a, d), (b, c), (b, d), (c, c), (c, d), (d, c), (d, d)],
    )


def test_queryIDBPredicateWithUndefinedEDB():
    db = facts([r("a", "b")])
    rules = [q(X, Y) <= p(X, Y)]
    ans = match3(db, rules)
    ans(q(X, Y), [])


def test_queryIDBPredicateWithExplicitIDBFact():
    # // Note that q is defined by a rule, but we also give an explicit fact.
    db = facts([r("a", "b"), q("b", "c")])
    rules = [q(X, Y) <= r(X, Y)]
    ans = match3(db, rules)
    ans(q(X, Y), [(a, b), (b, c)])


def test_queryZeroAryPredicates():
    program = [p() <= q(), r() <= [p(), s()], q(), s()]
    ans = match_relations(program)
    assert ans(q(), [q()])
    assert ans(p(), [p()])
    assert ans(s(), [s()])
    assert ans(r(), [r()])


# aaa
def test_querymutuallyrecursivepredicates():
    program = [
        p(X, Y, Z) <= q(X, Y, Z),
        q(X, Y, Z) <= p(Z, Y, X),
        p(X, Y, Z) <= r(X, Y, Z),
        r("a", "b", "c"),
    ]

    ans = match_relations(program)
    assert ans(p(X, Y, Z), [p("a", "b", "c"), p("c", "b", "a")])
    assert ans(p(X, "b", Y), [p("a", "b", "c"), p("c", "b", "a")])
    assert ans(p("a", X, "c"), [p("a", "b", "c")])
    assert ans(p(X, "c", Y), [])


def test_querymutuallyrecursivepredicates_no_facts():
    program = [p(X, Y, Z) <= q(X, Y, Z), q(X, Y, Z) <= p(X, Y, Z)]
    ans = match_relations(program)
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

    assert match_relations(program, one(X, Y, Z), [one("a", "b", "c")])


def test_queryIDBPredicatesWithConstants():
    program = [p("a", X) <= q(X, X), q("a", "a"), q("b", "b"), q("c", "d")]

    ans = match_relations(program)
    assert ans(p(Z, W), [p("a", "a"), p("a", "b")])
    assert ans(p("a", X), [p("a", "a"), p("a", "b")])

    program = [p(X, X) <= q(X, "a"), q("a", "a"), q("b", "b"), q("c", "d")]
    ans = match_relations(program)
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
    ans = match_relations(program)
    assert ans(p(), [p()])

    program = [p() <= [q("a", "b"), r("c", "d")], q("a", "b"), r("c", "d")]
    ans = match_relations(program)
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

    ans = match_relations(program)
    assert ans(tc(X, Y), [tc(0, 1), tc(1, 2), tc(2, 3)])

    program = program + [trigger()]
    ans = match_relations(program)
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
    ans = match_relations(program)
    assert ans(p(X), [p("a"), p("b")])
    program = [
        p(X, Y) <= q(Y, X, Y, X),
        q("a", "a", "a", "a"),
        q("a", "a", "a", "b"),
        q("a", "a", "b", "b"),
        q("a", "b", "b", "b"),
        q("b", "b", "b", "b"),
    ]

    ans = match_relations(program)

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

    ans = match_relations(program)
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
    ans = match_relations(program)
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
    ans = match_relations(program)
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

    ans = match_relations(program)
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
    ans = match_relations(program)
    assert ans(on(a), [on(a)])
    assert ans(on(_), [on(a), on(b)])
    program = [p() <= [q(_, _), r(_, _)], q(a, b), r(c, d)]
    ans = match_relations(program)
    assert ans(p(), [p()])


def test_testUnboundVariable1():
    a = "a"
    b = "b"
    with pytest.raises(DatalogValidationException):
        match_relations([p(X, b)], p(X, Y), [])
        match_relations([q(X, Y) <= p(X, b), p(a, b)], q(X, Y), [])


def test_testRulesWithTrue():
    a = "a"
    true = relation("true")
    false = relation("false")

    assert match_relations([false()], true(), [])
    assert match_relations([p(X) <= q(X), q(a)], true(), [])


def testEmptyProgram():
    anything = relation("anything")
    assert match_relations([], anything(), [])


def test_fact_to_dicts():
    rel = relation("rel")
    facts = [rel(a, b, c), rel(d, e, d)]
    query_vars = [Z, Y, X]
    from mercylog.core import facts_to_dict

    assert facts_to_dict(facts, query_vars) == {
        Z: ["a", "d"],
        Y: ["b", "e"],
        X: ["c", "d"],
    }
