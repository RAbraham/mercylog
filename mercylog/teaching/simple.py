from typing import *
from dataclasses import dataclass
from pprint import pprint
"""
Let's start with a simple Datalog Program. In Datalog, it would be:
man("Brad")
man("Abe")
person(X) <- man(X) # If someone is a man, then he is a person.

Let's define the above concepts.
`man` is like a table in the database, also called a base relation. `man("Bob")` is also called a `fact`

`person` is a derived relation, as it is derived from a base relation `man`, like a view in the database.
`person(X) <- man(X)` is called a rule.
X is a logical variable. It is used to refer to values abstractly. So man(X) could be used to abstractly refer to all man relations.

"""

"""
Let's first define a logical variable. It can represent a value. A relation can hold either a variable or a value.
"""
"""
we can create a variable like this:
X = Variable('X')
"""
@dataclass(frozen=True)
class Variable:
    name: str


"""
A relation could be:
man("Bob")
parent("John", "Chester") # John is a parent of Chester

It could also be components of a rule e.g.
`man(X)` or `person(x)` in `person(X) <- man(X)`


So a relation has a name(e.g. parent) and a list of attributes(e.g. "John" and "Chester" or X). 
"""

@dataclass(frozen=True)
class Relation:
    """
    man("Bob) is Relation("man", ["Bob"])
    parent("John", "Chester") is Relation("parent", ["John", "Chester"])
    man(X) is Relation("man", [Variable("X")])

    """
    name: str
    attributes: List


"""
A rule could be:
- person(X) <- man(X) i.e. X is a person if he is man.
- father(X, Y) <- man(X), parent(X, Y) i.e. X is a father of Y if X is a man and X is the parent of Y

A rule has:
- a head relation which is on the left of the `<-` symbol e.g. person(X) or father(X, Y)
- a body of relations which is on the right of the `<-` symbol e.g. man(X) or parent(X, Y)

X are Y are logical variables. It represents values. For e.g. man(X) could be matched to man("Bob") so X could be equal to Bob 
"""
@dataclass
class Rule:
    head: Relation
    body: List[Relation]

"""
Let's start with a simple query. No rules, just facts. Given:
man("Abe)
man("Bob")
woman("Abby")

Query:
man(X) # Find me all men 

The query should return:
Ans: [man("Bob"), man("George")]

This would be similar to a SQL query `select * from man`

Here's how I would compose it in Python
"""
X = Variable('X')
abe = Relation("man", ["Abe"])
bob = Relation("man", ["Bob"])
abby = Relation("woman", ["Abby"])
database = [abe, bob, abby]
no_rules = []
query = Relation("man", [X])


"""
The simplest run would iterate through all the facts and collect those which match the query
assert simplest_run(database, rules, query) == [fact1, fact2]
"""

"""
`name_match`. A fact matches a query if the fact and query match in relation name. 
"""
def name_match(fact, query):
    return fact.name == query.name

def filter_facts(database, query, match):
    return [fact for fact in database if match(fact, query)]


def run_simplest(database, rules, query):
    return filter_facts(database, query, name_match) 



assert run_simplest(database, no_rules, query) == [abe, bob]

"""
Let's add two tuple facts
parent("Abe", "Bob") # Abe is a parent of Bob
parent("Abby", "Bob")
parent("Bob", "Carl")
parent("Bob", "Connor")
parent("Beatrice", "Carl")

I may want to query who are the parents of Carl
Query:
parent(X, "Carl") # Should return [parent("Bob", "Carl"), parent("Beatrice", "Carl")

The beauty of Datalog is that you can ask the inverse without additional code e.g. Who are the children of Bob
parent("Bob", X) # Should return [parent("Bob", "Carl"), parent("Bob", "Connor")]


parent(X, "Carl") is similar to select * from parent where child = "Carl" if there was a table parent with columns `parent` and `child`)


"""

"""
Let's code that up. I'm just going to make a helper function to make it easy to express a parent relation
"""
parent = lambda parent, child: Relation("parent", [parent, child])
database = [
    parent("Abe", "Bob"), # Abe is a parent of Bob
    parent("Abby", "Bob"),
    parent("Bob", "Carl"),
    parent("Bob", "Connor"),
    parent("Beatrice", "Carl")
]


"""
Every value in the query should match the value in the fact if they are at the same position within the arguments
"""

def query_variable_match(fact, query):
    if fact.name != query.name:
        return False

    # TODO: zip is duplicated?
    for query_attribute, fact_attribute in zip(query.attributes, fact.attributes):
        if not isinstance(query_attribute, Variable) and query_attribute != fact_attribute :
                return False
    return True  

assert query_variable_match(parent("A", "Bob"), parent(X, "Bob") ) == True
assert query_variable_match(parent("A", "Bob"), parent("A", X)) == True
assert query_variable_match(parent("A", "NoMatch"), parent(X, "Bob") ) == False 



def run_with_filter(database, rules, query):
    return filter_facts(database, query, query_variable_match)


filtered_result1 =  run_with_filter(database, [], parent(X, "Carl")) 
assert filtered_result1 == [parent("Bob", "Carl"), parent("Beatrice", "Carl")]

filtered_result2 =  run_with_filter(database, [], parent("Bob", X)) 
assert filtered_result2 == [parent("Bob", "Carl"), parent("Bob", "Connor")]


"""
Let's add a rule to our program
man("Bob")
man("George")
animal("Tiger")
human(X) <- man(X) # You are human if you are man.

Query:
human(X) # Find me all humans

The query should return:
Ans: [human("Bob"), human("George")]

"""
man = lambda x: Relation("man", [x])
animal = lambda x: Relation("animal", [x])
human = lambda x: Relation("human", [x])
X = Variable("X")

head = human(X) 
body = [man(X)]
human_rule = Rule(head, body) # No Pun Intended when first written
database = [
    man("Abe"),
    man("Bob"),
    animal("Tiger")
]
rules = [human_rule]
query = human(X)

"""
The simplest rule match. For each rule, for each relation in it's body, if it matches with any of the facts in the database,
then get the attributes of that fact and transfer it to the head.

"""
def _run_simple(rules_evaluator, match, database, rules, query):
    inferred_facts = []
    for rule in rules:
        facts = rules_evaluator(rule, database)
        inferred_facts.extend(facts)
    
    knowledgebase = inferred_facts + database
    return filter_facts(knowledgebase, query, match)

# TODO: Delete _run_simple_conjunction after debugging
def _run_simple_conjunction(rules_evaluator, match, database, rules, query):
    inferred_facts = []
    for rule in rules:
        print("Evaluating rule:" + str(rule))
        facts = rules_evaluator(rule, database)
        print('Inferred Facts:' + str(facts))
        inferred_facts.extend(facts)
    
    knowledgebase = inferred_facts + database
    return filter_facts(knowledgebase, query, match)


def run_simplest_rule(database, rules, query):
    return _run_simple(evaluate_simplest_rule, query_variable_match, database, rules, query)

def evaluate_simplest_rule(rule: Rule, database: List[Relation]) -> List[Relation]:
    relation = rule.body[0] # we are only considering single clause bodies
    attributes = match_relation_and_database(database, relation)

    return [Relation(rule.head.name, list(attr.values())) for attr in attributes]

def match_relation_and_database(database, relation) -> List[Tuple]:
    inferred_attributes = []
    for fact in database:
        attributes = match_relation_and_fact(relation, fact)
        if attributes:
            inferred_attributes.append(attributes)
    return inferred_attributes

# def match_relation_and_fact(relation: Relation, fact: Relation) -> Optional[Tuple]:
#     if relation.name == fact.name:
#         return tuple(fact.attributes)

def match_relation_and_fact(relation: Relation, fact: Relation) -> Optional[Dict]:
    if relation.name == fact.name:
        return dict(zip(relation.attributes, fact.attributes))


simplest_rule_result = run_simplest_rule(database, rules, query)
assert simplest_rule_result == [human("Abe"), human("Bob")]

"""
Next, we introduce logical AND. i.e. Given
- echange examples of conjunction with father(X, Y) <= parent(X,Y), male(X)
parent("Abe", "Bob"), # Abe is a parent of Bob
parent("Abby", "Bob"),
parent("Bob", "Carl"),
parent("Bob", "Connor"),
parent("Beatrice", "Carl"),
man("Abe"),
man("Bob"),
woman("Abby"),
woman("Beatrice")

We'd like to find all the fathers in the house. A person is a father if he is a parent and he is a man.
father(X, Y) <- parent(X, Y), man(X)

"""
X = Variable("X")
Y = Variable("Y")
woman = lambda x: Relation("woman", [x])
father = lambda x, y: Relation("father", [x, y])

database = [
    parent("Abe", "Bob"), # Abe is a parent of Bob
    parent("Abby", "Bob"),
    parent("Bob", "Carl"),
    parent("Bob", "Connor"),
    parent("Beatrice", "Carl"),
    man("Abe"),
    man("Bob"),
    woman("Abby"),
    woman("Beatrice")
]

father_rule = Rule(father(X, Y), [parent(X, Y), man(X)])
rules = [father_rule]
query = father(X, Y)

"""
Next, we introduce logical AND. i.e. Given:

loves_datalog("Rajiv")
loves_datalog("Rich")
loves_datalog("John")
boring("Rajiv")
boring("John")

avoid_at_party(X) <- loves_datalog(X), boring(X) 

Query:
avoid_at_party(X) # This should return [avoid_at_party("Rajiv"), avoid_at_party("John")]

"""
# X = Variable("X")
# rajiv_loves_datalog = Relation("loves_datalog", ["Rajiv"])
# rich_loves_datalog = Relation("loves_datalog", ["Rich"])
# john_loves_datalog = Relation("loves_datalog",["John"] )
# rajiv_is_boring = Relation("boring", ["Rajiv"])
# john_is_boring = Relation("boring", ["John"])
# # avoid_at_party(X) <- loves_datalog(X), boring(X)
# avoid_head = Relation('avoid_at_party', [X])
# avoid_body = [Relation("loves_datalog", [X]), Relation("boring", [X])]
# avoid_rule = Rule(avoid_head, avoid_body)

# database = [rajiv_loves_datalog, rich_loves_datalog, john_loves_datalog, rajiv_is_boring, john_is_boring]
# rules = [avoid_rule]
"""
Similar as `run_simplest_rule` but when we match the body to the facts, we have to check if the attributes match for the entire body,
"""
def run_conjunction(database, rules, query):
    return _run_simple_conjunction(evaluate_rule_with_conjunction, query_variable_match, database, rules, query)

def evaluate_rule_with_conjunction(rule: Rule, database: List[Relation]) -> List[Relation]:
    body_attributes = []

    for relation in rule.body:
        _attributes = match_relation_and_database(database, relation)
        body_attributes.append(_attributes)

    # print('>>> Body Attributes')
    # pprint(body_attributes)
    attributes = conjunct(body_attributes)
    print('attributes after conjunction')
    pprint(attributes)

    aaa. extract the values from the attributes
    return [Relation(rule.head.name, list(attr)) for attr in attributes]

# def conjunct(body_attributes: List[List[Dict]]) -> Set:
#     _body_attributes = [tuple(l) for l in body_attributes]
#     pprint("Internal Body Attrs")
#     pprint(_body_attributes)
#     if not _body_attributes:
#         return set()
    
#     result_set = set(_body_attributes[0])
#     for ba in _body_attributes[1:]:
#         result_set = result_set.intersection(set(ba))
#     return result_set



def _conjunct_attributes(s1: Dict[Variable, Any], s2: Dict[Variable, Any]) -> bool:
    common_vars = set(s1.keys()).intersection(set(s2.keys()))
    return all([s1[c] == s2[c] for c in common_vars])
def pairings(s1: Dict[Variable, Any], s2: Dict[Variable, Any]) -> Dict[Variable, Any]:
    return {**s1, **s2}

def conjunct(body_attributes: List[List[Dict]]) -> List:
    _body_attributes = [tuple(l) for l in body_attributes]
    # pprint("Internal Body Attrs")
    # pprint(_body_attributes)
    result = []
    if not _body_attributes:
        return set()
    
    set1 = _body_attributes[0]
    set2 = _body_attributes[1]
    for s1 in set1:
        for s2 in set2:
            _c = _conjunct_attributes(s1, s2)
            if _c:
                result.append(pairings(s1, s2))
    
    return result
    

# query = Relation("avoid_at_party", [X])
# avoid_rajiv = Relation("avoid_at_party", ["Rajiv"])

# avoid_x = Relation("avoid_at_party", ["X"])
# avoid_john = Relation("avoid_at_party", ["John"])

# avoid_results = run_conjunction(database, rules, query)
# assert avoid_rajiv in avoid_results
# assert avoid_john in avoid_results

# ==============================================================

conjunction_results = run_conjunction(database, rules, query)
print('------ COnjunct results')
pprint(conjunction_results)

"""
Next, we introduce the reason why we are interested in Datalog. So far, everthing we have done is easily expressed in other languages like SQL as well. Datalog has the distinctive feature of intuitively capturing hierarchies or recursion. E.g.

parent("A", "B") # A is the parent of B
parent("B", "C")
parent("C", "D")
parent("AA", "BB")
parent("BB", "CC")

ancestor(X, Y) <= parent(X, Y)
ancestor(X, Z) <= parent(X, Y), ancestor(Y, Z)

Query:
ancestor(X, Y)
# Should return all the parents above as ancestors 
ancestor("A", "B") # A is the ancestor of B
ancestor("B", "C")
ancestor("C", "D")
ancestor("AA", "BB")
ancestor("BB", "CC")

It's going to start looking a bit ugly so let's define helper methods
"""
ancestor = lambda ancestor, descendant: Relation('ancestor', [Variable(ancestor), Variable(descendant)])

database = [parent("A", "B"), parent("B", "C"), parent("C", "D"), parent("AA", "BB"), parent("BB", "CC")]


X = Variable("X")
Y = Variable("Y")
Z = Variable("Z")
# ancestor(X, Y) <= parent(X, Y)
ancestor_rule_base = Rule(ancestor(X, Y), [parent(X, Y)])
# ancestor(X, Z) <= parent(X, Y), ancestor(Y, Z)
ancestor_rule_recursive = Rule(ancestor(X, Z), [parent(X, Y), ancestor(Y, Z)])

no_rules = [ancestor_rule_base, ancestor_rule_recursive]

"""
We define the evaluation 
"""

# def run_recursive(database, rules, query):
#     return _run_recursive(evaluate_recursive_rule, database, rules, query)


# def _run_recursive():
#     pass

# def evaluate_recursive_rule(rule: Rule, database: List[Relation]) -> List[Relation]:
#     pass 

"""
Let's define the query
"""
# query = ancestor(X, Y)

# recursive_result = run_recursive(database, rules, query)
# expected_result = [ancestor("A", "B"), ancestor("B", "C"), ancestor("C", "D"), ancestor("AA", "BB"), ancestor("BB", "CC")]

# for a in expected_result:
#     assert a in recursive_result, f"{a} not in {recursive_result}"

"""
Next, we introduce logical OR
human if you are man or if you are woman
"""


print('==================================== All Tests Pass ==================================================')