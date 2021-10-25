import pytest
import pandas as pd
from mercylog import db, R, V, or_, and_, eq
from mercylog.df import row
from tests.abcdatalog.helper import assert_df

from tests.util import assert_df, a_df

PEOPLE_COLUMNS = ["name", "name2", "rel"]

_parent = lambda parent, child: [parent, child, "parent"]
X = V.X
Y = V.Y
Z = V.Z


def test_user_api_filter():
    rows = [["Abe", "M"], ["Bob", "M"], ["Abby", "F"]]
    a_df = pd.DataFrame(rows, columns=["name", "gender"])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=["X"])

    ds = db(a_df)
    # select males
    males = ds([row(name=X, gender="M")])
    assert_df(males.df(), exp_df)


def test_single_body_rule():
    X = V.X
    rows = [["Abe", "man"], ["Bob", "man"], ["Samba", "animal"]]
    a_df = pd.DataFrame(rows, columns=["name", "species"])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=["X"])

    # Then
    ds = db(a_df)
    man = R.man(X) << row(name=X, species="man")
    human = ds([man, R.man(X)])
    assert_df(human.df(), exp_df)


def test_conjunction():
    man = lambda person: [person, "AA", "man"]
    woman = lambda person: [person, "AA", "woman"]
    X = V.X
    Y = V.Y
    Z = V.Z

    rows = [
        _parent("Abe", "Bob"),  # Abe is a parent of Bob
        _parent("Abby", "Bob"),
        _parent("Bob", "Carl"),
        _parent("Bob", "Connor"),
        _parent("Beatrice", "Carl"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice"),
    ]
    a_df = pd.DataFrame(rows, columns=PEOPLE_COLUMNS)
    exp_df = pd.DataFrame(
        [["Abe", "Bob"], ["Bob", "Carl"], ["Bob", "Connor"]], columns=["X", "Y"]
    )

    # Then test binary conjunction
    d = db(a_df)
    rules = [
        R.man(X) << row(name=X, rel="man"),
        R.parent(X, Y) << row(name=X, name2=Y, rel="parent"),
        R.father(X, Y) << and_(R.man(X), R.parent(X, Y)),
    ]
    queries = rules + [R.father(X, Y)]
    fathers = d(queries)
    assert_df(fathers.df(), exp_df)

    # Test n-ary conjunction
    grandfather_rule = R.grandfather(X, Y) << and_(
        R.man(X), R.parent(X, Z), R.parent(Z, Y)
    )
    rules = rules + [grandfather_rule]
    gf_d = d(rules + [R.grandfather(X, Y)])
    gf_rows = [["Abe", "Carl"], ["Abe", "Connor"]]
    exp_gf_df = pd.DataFrame(gf_rows, columns=["X", "Y"])
    assert_df(gf_d.df(), exp_gf_df)


def test_disjunction():
    rows = [
        ["Tiger", "animal"],
        ["Abe", "man"],
        ["Bob", "man"],
        ["Abby", "woman"],
        ["Beatrice", "woman"],
    ]
    a_df = pd.DataFrame(rows, columns=["name", "species"])
    exp_rows = ["Abe", "Bob", "Abby", "Beatrice"]
    exp_df = pd.DataFrame(exp_rows, columns=["X"])
    d = db(a_df)

    base_rules = [
        R.man(X) << row(name=X, species="man"),
        R.woman(X) << row(name=X, species="woman"),
    ]
    rules = [
        R.human(X) << R.man(X),
        R.human(X) << R.woman(X),
    ]
    query = [R.human(X)]
    humans = d(base_rules + rules + query)
    assert_df(humans.df(), exp_df)

    # Or Clause
    or_rules = [R.human(X) << or_(R.man(X), R.woman(X))]
    humans_or = d(base_rules + or_rules + query)
    assert_df(humans_or.df(), exp_df)


def test_recursion():
    database = [
        _parent("A", "B"),
        _parent("B", "C"),
        _parent("C", "D"),
        _parent("AA", "BB"),
        _parent("BB", "CC"),
    ]
    df = pd.DataFrame(database, columns=PEOPLE_COLUMNS)
    base = [
        R.parent(X, Y) << row(name=X, name2=Y, rel="parent"),
    ]
    rules = [
        R.ancestor(X, Y) << R.parent(X, Y),
        R.ancestor(X, Z) << and_(R.parent(X, Y), R.ancestor(Y, Z)),
    ]
    """
    or 
    rules = [
        R.ancestor(X,Y) << or_(R.parent(X,Y),
                               and_(R.parent(X, Z),
                                    R.parent(Z, Y)))
    ]
    """

    query = R.ancestor(X, Y)

    d = db(df)
    all_rules = base + rules
    exp_d = d(all_rules + [query])

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    AA = "AA"
    BB = "BB"
    CC = "CC"
    exp_rows = [
        [A, B],
        [B, C],
        [C, D],
        [AA, BB],
        [BB, CC],
        [A, C],
        [B, D],
        [AA, CC],
        [A, D],
    ]
    expected_result = pd.DataFrame(exp_rows, columns=["X", "Y"])

    assert_df(exp_d.df(), expected_result)

    new_rule = R.main(X, Y) << and_(R.ancestor(X, Y), eq(X, "AA"), eq(Y, "C"))

    d2 = d(all_rules + [new_rule] + [R.main(X, Y)])
    assert_df(d2.df(), a_df({}))
    d3 = d(all_rules + [R.ancestor(X, "C")])
    assert_df(d3.df(), a_df({"X": ["A", "B"]}))
    d4 = d(all_rules + [R.ancestor("AA", X)])
    assert_df(d4.df(), a_df({"X": ["BB", "CC"]}))
    rules = rules + [
        R.intermediate(Z, X, Y) << and_(R.ancestor(X, Z), R.ancestor(Z, Y))
    ]
    d5 = d(base + rules + [R.intermediate(Z, "A", "D")])
    assert_df(d5.df(), a_df({"Z": ["B", "C"]}))


def test_facts_from_rules():
    # Normally, we pass facts through a dataframe. But sometimes, a fact may just be needed to assert something
    # about the context/environment. So we pass that in the rules section
    exp_data = [["adam"]]
    exp_df = pd.DataFrame(data=exp_data, columns=["X"])
    rules = [
        R.father("adam", "kane"),  # This is the global fact or assertion
        R.parent(V.X, V.Parent) << R.father(V.X, V.Parent),
        R.parent(V.X, "kane"),
    ]
    ds = db()
    result = ds(rules)
    assert_df(result.df(), exp_df)


# When you consider variables
# def test_variables():
#     database = [
#         parent("A", "B"),
#         parent("B", "C"),
#         parent("C", "D"),
#         parent("AA", "BB"),
#         parent("BB", "CC"),
#     ]
#
#     ancestor_rule_base = ancestor(X, Y) <= parent(X, Y)
#     ancestor_rule_recursive = ancestor(X, Z) <= [parent(X, Y), ancestor(Y, Z)]
#
#     intermediate_rule = intermediate(Z, X, Y) <= [ancestor(X, Z), ancestor(Z, Y)]
#
#     rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
#     query = [intermediate(Z, X, Y)]
#     from functools import partial
#
#     run_var = partial(run, database, rules, query)
#
#     xs = ["A", "A", "B", "A", "AA"]
#     ys = ["D", "C", "D", "D", "CC"]
#     zs = ["B", "B", "C", "C", "BB"]
#     assert_df(run_var(), a_df({X: xs, Y: ys, Z: zs}))
#     assert_df(run_var([X]), a_df({X: xs}))
#     assert_df(run_var([X, Y]), a_df({X: xs, Y: ys}))
#     assert_df(run_var([X, Y, Z]), a_df({X: xs, Y: ys, Z: zs}))
#


# TODO: query composition. df_ds(a_df)(query1)(query2)
