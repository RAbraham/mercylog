import pytest
import pandas as pd
from mercylog import db, R, V, Q
from tests.abcdatalog.helper import assert_df

# API
# ds = df(customer_df) # with many columns
# ds([
#     R.customer(Id, Name, Age) <= ds.row(customer_id=Id, name=Name, age=Age)
#     R.customer(Id, _,  Age) # R.customer(Id=Id, Age=Age) # or R.customer({Id, Age})
# ])


def test_user_api_filter():
    X = V.X
    rows = [["Abe", "M"], ["Bob", "M"], ["Abby", "F"]]
    a_df = pd.DataFrame(rows, columns=["name", "gender"])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=[X])

    ds = db(a_df)
    # select males
    males = ds([ds.row(name=X, gender="M")])
    assert_df(males.df(), exp_df)


def test_single_body_rule():
    X = V.X
    rows = [["Abe", "man"], ["Bob", "man"], ["Samba", "animal"]]
    a_df = pd.DataFrame(rows, columns=["name", "species"])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=[X])

    # Then
    ds = db(a_df)
    man = R.man(X) <= ds.row(name=X, species="man")
    human = ds([man, Q.man(X)])

    assert_df(human.df(), exp_df)


def test_conjunction():
    parent = lambda parent, child: [parent, child, "parent"]
    man = lambda person: [person, "AA", "man"]
    woman = lambda person: [person, "AA", "woman"]
    X = V.X
    Y = V.Y
    Z = V.Z

    rows = [
        parent("Abe", "Bob"),  # Abe is a parent of Bob
        parent("Abby", "Bob"),
        parent("Bob", "Carl"),
        parent("Bob", "Connor"),
        parent("Beatrice", "Carl"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice"),
    ]
    a_df = pd.DataFrame(rows, columns=["name", "name2", "rel"])
    exp_df = pd.DataFrame(
        [["Abe", "Bob"], ["Bob", "Carl"], ["Bob", "Connor"]], columns=[X, Y]
    )

    # Then test binary conjunction
    d = db(a_df)
    rules = [
        R.man(X) <= d.row(name=X, rel="man"),
        R.parent(X, Y) <= d.row(name=X, name2=Y, rel="parent"),
        R.father(X, Y) <= [R.man(X), R.parent(X, Y)],
    ]
    queries = rules + [Q.father(X, Y)]
    fathers = d(queries)
    assert_df(fathers.df(), exp_df)

    # Test n-ary conjunction
    grandfather_rule = R.grandfather(X, Y) <= [R.man(X), R.parent(X, Z), R.parent(Z, Y)]
    rules = rules + [grandfather_rule]
    gf_d = d(rules + [R.grandfather(X, Y)])
    gf_rows = [["Abe", "Carl"], ["Abe", "Connor"]]
    exp_gf_df = pd.DataFrame(gf_rows, columns=[X, Y])
    assert_df(gf_d.df(), exp_gf_df)


def test_disjunction():
    X = V.X
    rows = [
        ["Tiger", "animal"],
        ["Abe", "man"],
        ["Bob", "man"],
        ["Abby", "woman"],
        ["Beatrice", "woman"],
    ]
    a_df = pd.DataFrame(rows, columns=["name", "species"])
    exp_rows = ["Abe", "Bob", "Abby", "Beatrice"]
    exp_df = pd.DataFrame(exp_rows, columns=[X])
    d = db(a_df)

    base_rules = [
        R.man(X) <= d.row(name=X, species="man"),
        R.woman(X) <= d.row(name=X, species="woman"),
    ]
    queries = base_rules + [
        R.human(X) <= R.man(X),
        R.human(X) <= R.woman(X),
    ]
    humans = d(queries + [R.human(X)])
    assert_df(humans.df(), exp_df)

    # Or Clause
    or_queries = [
        R.human(X) <= or_(R.man(X), R.woman(X))
    ]

    pass


# TODO: query composition. df_ds(a_df)(query1)(query2)
