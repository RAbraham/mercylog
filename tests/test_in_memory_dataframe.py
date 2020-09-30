import pytest
from mercylog.data_sources.in_memory import (
    Variable,
    run,
    query_variable_match,
    query_variables,
)
from mercylog.types import relation
import pandas as pd

X = Variable("X")
Y = Variable("Y")
Z = Variable("Z")


def a_df(a_dict):
    return pd.DataFrame(a_dict)


def test_query_variables():
    query = [man(X)]
    assert query_variables(query) == {X}
    query = [parent(X, "Carl")]
    assert query_variables(query) == {X}
    query = [man(X), parent(X, Z), parent(Z, Y)]
    assert query_variables(query) == {X, Y, Z}
    # TODO: we have to check if vars is passed, it is a valid subset of the query?
    # TODO: What about don't care variable i.e. m._


def assert_df(df1, df2):
    df1_dicts = df1.to_dict("records")
    df2_dicts = df2.to_dict("records")
    for item in df1_dicts:
        if item not in df2_dicts:
            assert False, f"{item} not in df2"
    for item in df2_dicts:
        if item not in df1_dicts:
            assert False, f"{item} not in df1"


def test_relation_filter():
    abe = man("Abe")
    bob = man("Bob")
    database = [abe, bob, woman("Abby")]

    assert_df(run(database, [], [man(X)]), a_df({X: ["Abe", "Bob"]}))


def test_query_variable_match():
    assert query_variable_match(parent("A", "Bob"), parent(X, "Bob")) == True
    assert query_variable_match(parent("A", "Bob"), parent("A", X)) == True
    assert query_variable_match(parent("A", "NoMatch"), parent(X, "Bob")) == False


def test_filter():
    database = [
        parent("Abe", "Bob"),  # Abe is a parent of Bob
        parent("Abby", "Bob"),
        parent("Bob", "Carl"),
        parent("Bob", "Connor"),
        parent("Beatrice", "Carl"),
    ]
    parents_carl = run(database, [], [parent(X, "Carl")])
    assert_df(parents_carl, a_df({X: ["Bob", "Beatrice"]}))

    children_bob = run(database, [], [parent("Bob", X)])
    assert_df(children_bob, a_df({X: ["Carl", "Connor"]}))


def test_single_body_rule():
    human_rule = human(X) <= man(X)
    database = [man("Abe"), man("Bob"), animal("Tiger")]

    simplest_rule_result = run(database, [human_rule], [human(X)])
    assert_df(simplest_rule_result, a_df({X: ["Abe", "Bob"]}))


def test_conjunction():

    database = [
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

    father_rule = father(X, Y) <= [man(X), parent(X, Y)]
    rules = [father_rule]
    query = father(X, Y)
    simple_conjunct_rules = [human(X) <= man(X)]
    result1 = run(database, simple_conjunct_rules, [human(X)])
    assert_df(result1, a_df({X: ["Abe", "Bob"]}))
    assert_df(
        run(database, rules, [query]),
        a_df({X: ["Abe", "Bob", "Bob"], Y: ["Bob", "Carl", "Connor"]}),
    )


def test_n_body_rules():
    database = [
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
    grandfather = relation("grandfather")
    grandfather_rule = grandfather(X, Y) <= [man(X), parent(X, Z), parent(Z, Y)]
    assert_df(
        run(database, [grandfather_rule], [grandfather(X, Y)]),
        a_df({X: ["Abe", "Abe"], Y: ["Carl", "Connor"]}),
    )


def test_disjunction():
    database = [
        animal("Tiger"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice"),
    ]

    man_rule = human(X) <= man(X)
    woman_rule = human(X) <= woman(X)

    rules = [man_rule, woman_rule]
    query = human(X)
    result = run(database, rules, [query])
    exp = a_df({X: ["Abe", "Bob", "Abby", "Beatrice"]})
    assert_df(result, exp)


def test_recursion():

    database = [
        parent("A", "B"),
        parent("B", "C"),
        parent("C", "D"),
        parent("AA", "BB"),
        parent("BB", "CC"),
    ]

    ancestor_rule_base = ancestor(X, Y) <= parent(X, Y)
    ancestor_rule_recursive = ancestor(X, Z) <= [parent(X, Y), ancestor(Y, Z)]

    rules = [ancestor_rule_base, ancestor_rule_recursive]

    query = ancestor(X, Y)

    recursive_result = run(database, rules, [query])

    expected_result = a_df(
        {
            X: ["A", "B", "C", "AA", "BB", "A", "B", "AA", "A"],
            Y: ["B", "C", "D", "BB", "CC", "C", "D", "CC", "D"],
        }
    )

    assert_df(recursive_result, expected_result)

    query = ancestor("AA", "C")

    assert_df(run(database, rules, [query]), a_df({}))

    query = ancestor(X, "C")
    assert_df(run(database, rules, [query]), a_df({X: ["A", "B"]}))

    query = ancestor("AA", X)
    assert_df(run(database, rules, [query]), a_df({X: ["BB", "CC"]}))

    # intermediate
    intermediate_rule = intermediate(Z, X, Y) <= [ancestor(X, Z), ancestor(Z, Y)]

    rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
    query = intermediate(Z, "A", "D")
    assert_df(run(database, rules, [query]), a_df({Z: ["B", "C"]}))


def test_variables():
    database = [
        parent("A", "B"),
        parent("B", "C"),
        parent("C", "D"),
        parent("AA", "BB"),
        parent("BB", "CC"),
    ]

    ancestor_rule_base = ancestor(X, Y) <= parent(X, Y)
    ancestor_rule_recursive = ancestor(X, Z) <= [parent(X, Y), ancestor(Y, Z)]

    intermediate_rule = intermediate(Z, X, Y) <= [ancestor(X, Z), ancestor(Z, Y)]

    rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
    query = [intermediate(Z, X, Y)]
    print(">>Test Var")
    """
    Y   Z   X
0   D   B   A
1   C   B   A
2   D   C   B
3   D   C   A
4  CC  BB  AA
    """
    from functools import partial

    run_var = partial(run, database, rules, query)

    xs = ["A", "A", "B", "A", "AA"]
    ys = ["D", "C", "D", "D", "CC"]
    zs = ["B", "B", "C", "C", "BB"]
    assert_df(run_var(), a_df({X: xs, Y: ys, Z: zs}))
    assert_df(run_var([X]), a_df({X: xs}))
    assert_df(run_var([X, Y]), a_df({X: xs, Y: ys}))
    assert_df(run_var([X, Y, Z]), a_df({X: xs, Y: ys, Z: zs}))



parent = relation("parent")

man = relation("man")

woman = relation("woman")

human = relation("human")

animal = relation("animal")


father = relation("father")
ancestor = relation("ancestor")

intermediate = relation("intermediate")


# Test Cases
# rule(X, Y) <= b("A", X), b1("A", Y)
