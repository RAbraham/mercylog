import pytest
from mercylog.data_sources.in_memory import Variable, Relation, run, query_variable_match, Rule
from mercylog.types import relation


X = Variable('X')
Y = Variable("Y")
Z = Variable("Z")

def test_relation_filter():
    abe = man("Abe")
    bob = man("Bob")
    database = {
        abe,
        bob,
        woman("Abby")}

    assert run(database, [], man(X)) == {abe, bob}

def test_query_variable_match():
    assert query_variable_match(parent("A", "Bob"), parent(X, "Bob") ) == True
    assert query_variable_match(parent("A", "Bob"), parent("A", X)) == True
    assert query_variable_match(parent("A", "NoMatch"), parent(X, "Bob") ) == False 

def test_filter():
    database = {
        parent("Abe", "Bob"), # Abe is a parent of Bob
        parent("Abby", "Bob"),
        parent("Bob", "Carl"),
        parent("Bob", "Connor"),
        parent("Beatrice", "Carl")
    }
    parents_carl =  run(database, [], parent(X, "Carl")) 
    assert parents_carl == {parent("Bob", "Carl"), parent("Beatrice", "Carl")}

    children_bob =  run(database, [], parent("Bob", X)) 
    assert children_bob == {parent("Bob", "Carl"), parent("Bob", "Connor")}


def test_single_body_rule():
    human_rule = human(X) <= man(X) 
    database = {
        man("Abe"),
        man("Bob"),
        animal("Tiger")
    }

    simplest_rule_result = run(database, [human_rule], human(X))
    assert simplest_rule_result == {human("Abe"), human("Bob")}


def test_conjunction():

    database = {
        parent("Abe", "Bob"), # Abe is a parent of Bob
        parent("Abby", "Bob"),
        parent("Bob", "Carl"),
        parent("Bob", "Connor"),
        parent("Beatrice", "Carl"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice")
    }

    father_rule = father(X, Y) <= [man(X), parent(X, Y)]
    rules = [father_rule]
    query = father(X, Y)
    simple_conjunct_rules = [human(X) <= man(X)]
    assert run(database, simple_conjunct_rules, human(X)) == {human("Abe"), human("Bob")}
    assert run(database, rules, query) == {father("Abe", "Bob"), father("Bob", "Carl"), father("Bob", "Connor")}

def test_n_body_rules():
    database = {
        parent("Abe", "Bob"), # Abe is a parent of Bob
        parent("Abby", "Bob"),
        parent("Bob", "Carl"),
        parent("Bob", "Connor"),
        parent("Beatrice", "Carl"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice")
    }
    grandfather = relation("grandfather")
    grandfather_rule = grandfather(X, Y) <= [man(X), parent(X, Z), parent(Z, Y)]
    assert run(database, [grandfather_rule], grandfather(X, Y)) == {grandfather("Abe", "Carl"), grandfather("Abe", "Connor")}

    

def test_disjunction():
    database = {
        animal("Tiger"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice")
    }

    man_rule = human(X) <= man(X)
    woman_rule = human(X) <= woman(X)
    
    rules = [man_rule, woman_rule]
    query = human(X)

    assert run(database, rules, query) == {
        human("Abe"),
        human("Bob"),
        human("Abby"),
        human("Beatrice")
    }


def test_recursion():

    database = {
        parent("A", "B"), 
        parent("B", "C"), 
        parent("C", "D"), 
        parent("AA", "BB"),
        parent("BB", "CC")
    }


    X = Variable("X")
    Y = Variable("Y")
    Z = Variable("Z")
    ancestor_rule_base = ancestor(X, Y) <= parent(X, Y)
    ancestor_rule_recursive = ancestor(X, Z) <= [parent(X, Y), ancestor(Y, Z)] 

    rules = [ancestor_rule_base, ancestor_rule_recursive]

    query = ancestor(X, Y)

    recursive_result = run(database, rules, query)

    expected_result = {
        ancestor("A", "B"), 
        ancestor("B", "C"), 
        ancestor("C", "D"), 
        ancestor("AA", "BB"),
        ancestor("BB", "CC"),
        ancestor("A", "C"),
        ancestor("B", "D"),
        ancestor("AA", "CC"),
        ancestor("A", "D")
    }

    assert recursive_result == expected_result, f"{recursive_result} not equal to {expected_result}"

    query = ancestor("AA", "C")

    assert run(database, rules, query) == set()
    query = ancestor(X, "C")

    assert run(database, rules, query) == {ancestor("A", "C"), ancestor("B", "C")}
    query = ancestor("AA", X)

    assert run(database, rules, query) == {ancestor("AA", "BB"), ancestor("AA", "CC")}

    # intermediate 
    intermediate_rule = intermediate(Z, X, Y) <= [ancestor(X, Z), ancestor(Z, Y)]

    rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
    query = intermediate(Z, "A", "D")

    assert run(database, rules, query) == {intermediate("B", "A", "D"), intermediate("C", "A", "D")}


parent = relation("parent")

man = relation("man")

woman = relation("woman")

human = relation("human")

animal = relation("animal")


father = relation('father')
ancestor = relation("ancestor")

intermediate = relation("intermediate")