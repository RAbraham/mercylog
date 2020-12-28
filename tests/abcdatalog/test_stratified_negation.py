import pytest
from mercylog.abcdatalog.ast.validation.datalog_validation_exception import (
    DatalogValidationException,
)

from mercylog.types import relation, _, eq, not_eq

from tests.abcdatalog.helper import (
    match_relations,
    X,
    Y,
    Z,
    p,
    q,
    r,
    s,
    a,
    b,
    c,
    edge,
    tc,
    node,
    not_tc,
)
from tests.data.abcdatalog.related import (
    adria,
    ancestor,
    barrett,
    carson,
    check, deidra,
    eldon,
    fern,
    gonzalo,
    harley,
    ignacia,
    kati,
    lauretta,
    mayra,
    noe,
    odell,
    reanna,
    same_generation,
    siblings,
    sona,
    terra,
    unrelated,
    ursula,
    virgilio,
)


def test_TestUnstratifiable1():
    program = [
        p() <= ~q(),
        q() <= ~p(),
    ]
    with pytest.raises(DatalogValidationException):
        match_relations(program, None, None)


def test_TestUnstratifiable2():
    edb = relation("edb")
    program = [p(X) <= [~q(X), edb(X)], q(X) <= [~p(X), edb(X)], edb(a)]
    with pytest.raises(DatalogValidationException):
        match_relations(program, None, None)


def test_TestStratifiable():
    program = [
        edge(a, b),
        edge(b, c),
        tc(a, c),
        tc(X, Y) <= edge(X, Y),
        tc(X, Y) <= [tc(X, Z), tc(Z, Y)],
        node(X) <= edge(X, _),
        node(X) <= edge(_, X),
        not_tc(X, Y) <= [node(X), node(Y), ~tc(X, Y)],
    ]
    ans = match_relations(program)
    assert ans(tc(X, Y), [tc(a, b), tc(b, c), tc(a, c)])
    assert ans(
        not_tc(X, Y),
        [
            not_tc(a, a),
            not_tc(b, b),
            not_tc(b, a),
            not_tc(c, c),
            not_tc(c, a),
            not_tc(c, b),
        ],
    )


def test_testNegatedUnboundVariable1():
    with pytest.raises(DatalogValidationException):
        match_relations([p() <= ~q(X, a)], p(), [])


def test_testNegatedUnboundVariable2():
    with pytest.raises(DatalogValidationException):
        match_relations([p(X) <= ~q(X, a)], p(), [])


def test_testNegatedUnboundVariable3():
    with pytest.raises(DatalogValidationException):
        match_relations([p() <= [~q(X, a), ~r(X)]], p(), [])


def test_testMultiLayeredNegation():
    program = [
        p() <= ~q(),
        q() <= ~r(),
        r() <= ~s(),
    ]
    assert match_relations(program, p(), [p()])


# // These next three tests assume that the engine being tested also supports
# // explicit unification.
def test_testExplicitUnification1():
    program = [p() <= [~q(X, b), eq(X, a)]]
    assert match_relations(program, p(), [p()])


def test_testExplicitUnification2():
    program = [p() <= [~q(X, b), not_eq(X, a)]]
    with pytest.raises(DatalogValidationException):
        match_relations(program, p(), [])


def test_testNegatedNoPositiveAtom():
    program = [p(a) <= ~q(a), p(b) <= [~q(X), eq(X, b)]]
    assert match_relations(program, p(X), [p(a), p(b)])


def test_testNegatedAtomFirst():
    n = relation("n")
    e = relation("e")
    unreach = relation("unreach")
    program = [
        n(a),
        n(b),
        n(c),
        e(a, b),
        e(b, c),
        r(X, Y) <= e(X, Y),
        r(X, Y) <= [e(X, Z), r(Z, Y)],
        unreach(X, Y) <= [~r(X, Y), n(X), n(Y)],
    ]
    assert match_relations(
        program,
        unreach(X, Y),
        [
            unreach(b, a),
            unreach(c, b),
            unreach(c, a),
            unreach(a, a),
            unreach(b, b),
            unreach(c, c),
        ],
    )


#
# @Test
# public void testRelated() throws DatalogValidationException {
def test_testRelated():
    from tests.data.abcdatalog.related import (
        related_data,
        check,
        siblings,
        _exp_data_siblings,
        ancestor,
        _exp_data_ancestors,
        same_generation,
        gonzalo,
        harley,
        eldon,
        fern,
        reanna,
        sona,
        terra,
        ursula,
    )

    program = related_data
    ans = match_relations(program)
    assert ans(check(X, Y), [])
    assert ans(siblings(X, Y), _exp_data_siblings)
    assert ans(ancestor(X, Y), _exp_data_ancestors)
    assert ans(
        same_generation(gonzalo, Y),
        [
            same_generation(gonzalo, harley),
            same_generation(gonzalo, eldon),
            same_generation(gonzalo, fern),
        ],
    )
    assert ans(
        same_generation(X, reanna),
        [
            same_generation(sona, reanna),
            same_generation(terra, reanna),
            same_generation(ursula, reanna),
        ],
    )
    assert ans(
        unrelated(adria, Y),
        [
            unrelated(adria, barrett),
            unrelated(adria, ignacia),
            unrelated(adria, kati),
            unrelated(adria, lauretta),
            unrelated(adria, mayra),
            unrelated(adria, noe),
            unrelated(adria, odell),
            unrelated(adria, reanna),
            unrelated(adria, sona),
            unrelated(adria, terra),
            unrelated(adria, ursula),
            unrelated(adria, virgilio),
        ],
    )

    assert ans(
        unrelated(X, odell),
        [
            unrelated(adria, odell),
            unrelated(barrett, odell),
            unrelated(carson, odell),
            unrelated(harley, odell),
            unrelated(gonzalo, odell),
            unrelated(deidra, odell),
            unrelated(eldon, odell),
            unrelated(fern, odell),
        ],
    )


# public void testRelated2() throws DatalogValidationException {
def test_testRelated2():
    from tests.data.abcdatalog.related2 import related_data as program, _exp_ancestors

    ans = match_relations(program)
    assert ans(check(X, Y), [])
    assert ans(
        siblings(X, Y),
        [
            siblings(carson, deidra),
            siblings(deidra, carson),
            siblings(harley, gonzalo),
            siblings(gonzalo, harley),
            siblings(eldon, fern),
            siblings(fern, eldon),
            siblings(noe, odell),
            siblings(odell, noe),
            siblings(reanna, sona),
            siblings(sona, reanna),
            siblings(terra, ursula),
            siblings(ursula, terra),
        ],
    )

    assert ans(ancestor(X, Y), _exp_ancestors)
    assert ans(
        same_generation(gonzalo, Y),
        [
            same_generation(gonzalo, harley),
            same_generation(gonzalo, eldon),
            same_generation(gonzalo, fern),
        ],
    )
    assert ans(
        same_generation(X, reanna),
        [
            same_generation(sona, reanna),
            same_generation(terra, reanna),
            same_generation(ursula, reanna),
        ],
    )
    assert ans(
        unrelated(adria, Y),
        [
            unrelated(adria, barrett),
            unrelated(adria, ignacia),
            unrelated(adria, kati),
            unrelated(adria, lauretta),
            unrelated(adria, mayra),
            unrelated(adria, noe),
            unrelated(adria, odell),
            unrelated(adria, reanna),
            unrelated(adria, sona),
            unrelated(adria, terra),
            unrelated(adria, ursula),
            unrelated(adria, virgilio),
        ],
    )
    assert ans(
        unrelated(X, odell),
        [
            unrelated(adria, odell),
            unrelated(barrett, odell),
            unrelated(carson, odell),
            unrelated(harley, odell),
            unrelated(gonzalo, odell),
            unrelated(deidra, odell),
            unrelated(eldon, odell),
            unrelated(fern, odell),
        ],
    )

