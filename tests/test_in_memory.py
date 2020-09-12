import pytest
from mercylog.data_sources.in_memory import Variable, Relation, run, query_variable_match, Rule


X = Variable('X')
Y = Variable("Y")

def test_relation_filter():
    abe = man("Abe")
    bob = man("Bob")
    database = {
        abe,
        bob,
        woman("Abby")}
    no_rules = [] 

    assert run(database, no_rules, man(X)) == {abe, bob}

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

    head = human(X) 
    body = [man(X)]
    human_rule = Rule(head, body) # No pun was intended
    database = {
        man("Abe"),
        man("Bob"),
        animal("Tiger")
    }
    rules = [human_rule]
    query = human(X)

    simplest_rule_result = run(database, rules, query)
    assert simplest_rule_result == {human("Abe"), human("Bob")}


def test_conjunction():
    woman = lambda x: Relation("woman", (x,))
    father = lambda x, y: Relation("father", (x, y))

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

    father_rule = Rule(father(X, Y), {parent(X, Y), man(X)})
    rules = [father_rule]
    query = father(X, Y)
    simple_conjunct_rules = [Rule(human(X), {man(X)})]
    assert run(database, simple_conjunct_rules, human(X)) == {human("Abe"), human("Bob")}
    assert run(database, rules, query) == {father("Abe", "Bob"), father("Bob", "Carl"), father("Bob", "Connor")}


def test_disjunction():
    database = {
        animal("Tiger"),
        man("Abe"),
        man("Bob"),
        woman("Abby"),
        woman("Beatrice")
    }

    man_rule = Rule(human(X), {man(X)})
    woman_rule = Rule(human(X), {woman(X)})
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
    # ancestor(X, Y) :- parent(X, Y)
    ancestor_rule_base = Rule(ancestor(X, Y), [parent(X, Y)])
    # ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)
    ancestor_rule_recursive = Rule(ancestor(X, Z), {parent(X, Y), ancestor(Y, Z)})

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

    intermediate = lambda intermediate, start, end: Relation("intermediate", (intermediate, start, end))
    intermediate_head = intermediate(Z, X, Y)
    intermediate_body = {ancestor(X, Z), ancestor(Z, Y)} 
    intermediate_rule = Rule(intermediate_head, intermediate_body)

    rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
    query = intermediate(Z, "A", "D")

    assert run(database, rules, query) == {intermediate("B", "A", "D"), intermediate("C", "A", "D")}


parent = lambda parent, child: Relation("parent", (parent, child))

man = lambda x: Relation("man", (x,))

human = lambda x: Relation("human", (x,))

animal = lambda x: Relation("animal", (x,))

woman = lambda x: Relation("woman", (x,))

animal = lambda x: Relation("animal", (x,))


ancestor = lambda ancestor, descendant: Relation('ancestor', (ancestor, descendant))