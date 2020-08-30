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

@dataclass(frozen=True, eq=True)
class Relation:
    """
    man("Bob) is Relation("man", ("Bob",))
    parent("John", "Chester") is Relation("parent", ("John", "Chester"))
    man(X) is Relation("man", (Variable("X"),))

    """
    name: str
    attributes: Tuple 


"""
A rule could be:
- person(X) <- man(X) i.e. X is a person if he is man.
- father(X, Y) <- man(X), parent(X, Y) i.e. X is a father of Y if X is a man and X is the parent of Y

A rule has:
- a head relation which is on the left of the `<-` symbol e.g. person(X) or father(X, Y)
- a body of relations which is on the right of the `<-` symbol e.g. man(X) or parent(X, Y)

X are Y are logical variables. It represents values. For e.g. man(X) could be matched to man("Bob") so X could be equal to Bob 
"""
@dataclass(frozen=True, eq=True)
class Rule:
    head: Relation
    body: Set[Relation]

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
abe = Relation("man", ("Abe",))
bob = Relation("man", ("Bob",))
abby = Relation("woman", ("Abby",))
database = {abe, bob, abby}
no_rules = [] 
query = Relation("man", (X,))


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
    return {fact for fact in database if match(fact, query)}


def run_simplest(database, rules, query):
    return filter_facts(database, query, name_match) 


assert run_simplest(database, no_rules, query) == {abe, bob}

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
parent = lambda parent, child: Relation("parent", (parent, child))
database = {
    parent("Abe", "Bob"), # Abe is a parent of Bob
    parent("Abby", "Bob"),
    parent("Bob", "Carl"),
    parent("Bob", "Connor"),
    parent("Beatrice", "Carl")
}


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
assert filtered_result1 == {parent("Bob", "Carl"), parent("Beatrice", "Carl")}

filtered_result2 =  run_with_filter(database, [], parent("Bob", X)) 
assert filtered_result2 == {parent("Bob", "Carl"), parent("Bob", "Connor")}


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
man = lambda x: Relation("man", (x,))
animal = lambda x: Relation("animal", (x,))
human = lambda x: Relation("human", (x,))
X = Variable("X")

head = human(X) 
body = {man(X)}
human_rule = Rule(head, body) # No Pun Intended when first written
database = {
    man("Abe"),
    man("Bob"),
    animal("Tiger")
}
rules = [human_rule]
query = human(X)

"""
The simplest rule match. For each rule, for each relation in it's body, if it matches with any of the facts in the database,
then get the attributes of that fact and transfer it to the head.

"""
def _run_simple(rules_evaluator, match, database, rules, query):
    knowledge_base = database
    for rule in rules:
        knowledge_base = knowledge_base.union(rules_evaluator(rule, database))
    
    return filter_facts(knowledge_base, query, match)

def run_simplest_rule(database, rules, query):
    return _run_simple(evaluate_simplest_rule, query_variable_match, database, rules, query)

def evaluate_simplest_rule(rule: Rule, database: List[Relation]) -> List[Relation]:
    relation = list(rule.body)[0] # we are only considering single clause bodies
    attributes = match_relation_and_database(database, relation)

    return [Relation(rule.head.name, tuple(attr.values())) for attr in attributes]


def match_relation_and_database(database, relation) -> List[Tuple]:
    inferred_attributes = []
    for fact in database:
        attributes = match_relation_and_fact(relation, fact)
        if attributes:
            inferred_attributes.append(attributes)
    return inferred_attributes


def match_relation_and_fact(relation: Relation, fact: Relation) -> Optional[Dict]:
    if relation.name == fact.name:
        return dict(zip(relation.attributes, fact.attributes))


simplest_rule_result = run_simplest_rule(database, rules, query)
# simplest_rule_result = run_conjunction(database, rules, query)
assert simplest_rule_result == {human("Abe"), human("Bob")}, f"result was {simplest_rule_result}"

"""
Next, we introduce logical AND. i.e. Given
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

"""
Similar as `run_simplest_rule` but when we match the body to the facts, we have to check if the attributes match for the entire body,
"""
def run_logical_operators(database, rules, query):
    return _run_simple(evaluate_rule_with_conjunction, query_variable_match, database, rules, query)

def evaluate_rule_with_conjunction(rule: Rule, database: List[Relation]) -> Set[Relation]:
    body_attributes = []

    for relation in rule.body:
        _attributes = match_relation_and_database(database, relation)
        body_attributes.append(_attributes)

    attributes = conjunct(body_attributes)
    
    return {Relation(rule.head.name, rule_attributes(rule.head, attr)) for attr in attributes}


def rule_attributes(relation: Relation, attr: Dict[Variable, Any]) -> Tuple:
    return tuple([attr[a] for a in relation.attributes])

def conjunct(body_attributes: List[List[Dict]]) -> List:
    result = []
    if len(body_attributes) == 1:
        return body_attributes[0]
    
    attr1 = body_attributes[0]
    attr2 = body_attributes[1]
    for a1 in attr1:
        for a2 in attr2:
            _c = has_common_value(a1, a2)
            if _c:
                result.append({**a1, **a2})
    
    return result
    

def has_common_value(s1: Dict[Variable, Any], s2: Dict[Variable, Any]) -> bool:
    common_vars = set(s1.keys()).intersection(set(s2.keys()))
    return all([s1[c] == s2[c] for c in common_vars])



conjunction_results = run_logical_operators(database, rules, query)
assert len(conjunction_results) == 3
assert father("Abe", "Bob") in conjunction_results
assert father("Bob", "Carl") in conjunction_results
assert father("Bob", "Connor") in conjunction_results

rules = [Rule(human(X), {man(X)})]
conjunction_result_simple_rule = run_logical_operators(database, rules, human(X))
assert conjunction_result_simple_rule == {human("Abe"), human("Bob")}

"""
Logical OR is just specifying two separate rules with the same head. E.g.
human(X) <= man(X)
human(X) <= woman(X)

"""
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



assert run_logical_operators(database, rules, query) == {
    human("Abe"),
    human("Bob"),
    human("Abby"),
    human("Beatrice")
}

"""
Next, we introduce the reason why we are interested in Datalog. Datalog has the distinctive feature of intuitively capturing hierarchies or recursion. E.g. we want to find all who are ancestors of someone

parent("A", "B") # A is the parent of B
parent("B", "C")
parent("C", "D")
parent("AA", "BB")
parent("BB", "CC")

# A parent X of Y is by definition an ancestor.
ancestor(X, Y) <= parent(X, Y)
# If you are a parent of Y and Y is an an ancestor, then you are an ancestor as well.
ancestor(X, Z) <= parent(X, Y), ancestor(Y, Z)

Query:
ancestor(X, Y)
# Should return all the parents above as ancestors 
ancestor("A", "B") # A is the ancestor of B
ancestor("A", "C") # A -> B -> C
ancestor("A", "D") # A -> B -> C -> D
ancestor("B", "C")
ancestor("B", "D") # B -> C -> D
ancestor("C", "D")
ancestor("AA", "BB")
ancestor("AA", "CC") # AA -> BB -> CC
ancestor("BB", "CC")

It's going to start looking a bit ugly so let's define helper methods
"""
ancestor = lambda ancestor, descendant: Relation('ancestor', (ancestor, descendant))

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
# ancestor(X, Y) <= parent(X, Y)
ancestor_rule_base = Rule(ancestor(X, Y), [parent(X, Y)])
# ancestor(X, Z) <= parent(X, Y), ancestor(Y, Z)
ancestor_rule_recursive = Rule(ancestor(X, Z), {parent(X, Y), ancestor(Y, Z)})

rules = [ancestor_rule_base, ancestor_rule_recursive]

"""
Alright, let's dive into this. What is different from run_conjunction? It's the hierarchy or recursion. If you see it as hierarchy(I'm visualizing this as a tree), one has to keep on going until we reach the top(or the bottom) of the tree. If we see it as a recursion, we keep on going till we hit the base case which terminates the recursion. So let's imagine how we would process the above example. In the first pass, we would do the simplest inference from base fact to derived fact using the base rule of ancestor(X, Y) <= parent(X, Y) 


Pass 1: Base Facts and Inferred facts i.e. KnowledgeBase1
parent("A", "B"), 
parent("B", "C"), 
parent("C", "D"), 
parent("AA", "BB"),
parent("BB", "CC")]
# ----------------- New inferred facts below --------------
ancestor("A", "B"), 
ancestor("B", "C"), 
ancestor("C", "D"), 
ancestor("AA", "BB"),
ancestor("BB", "CC")

Now that's done, we can focus on inference from a combination of inferred facts and base facts to new inferred facts using the recursive rule ancestor(X, Z) <= parent(X, Y), ancestor(Y, Z). For e.g. in KnowledgeBase1, we have parent("C","D") and ancestor("B", "C") , so we can infer the fact ancestor("B", "D") i.e grandparents. We keep on doing this till we get:

Pass 2: KnowledgeBase2
parent("A", "B"), 
parent("B", "C"), 
parent("C", "D"), 
parent("AA", "BB"),
parent("BB", "CC")
ancestor("A", "B"), 
ancestor("B", "C"), 
ancestor("C", "D"), 
ancestor("AA", "BB"),
ancestor("BB", "CC")
# ----------------- New inferred facts below --------------
ancestor("A", "C")
ancestor("B", "D")
ancestor("AA", "CC")

Do we stop? No, we have to keep on going till we find all the ancestors. Let's apply the rules to KnowledgeBase2 and get

Pass 3: KnowledgeBase3
parent("A", "B"), 
parent("B", "C"), 
parent("C", "D"), 
parent("AA", "BB"),
parent("BB", "CC")
ancestor("A", "B"), 
ancestor("B", "C"), 
ancestor("C", "D"), 
ancestor("AA", "BB"),
ancestor("BB", "CC")
ancestor("A", "C")
ancestor("B", "D")
ancestor("AA", "CC")
# ----------------- New inferred facts below --------------
ancestor("A", "D")

i.e A is the great grand parent of D

Do we stop? Yes(if you look at the above example), but the computer does not know that. There could be new inferred facts, so let's try again for KnowledgeBase4

Pass 4: KnowledgeBase4
parent("A", "B"), 
parent("B", "C"), 
parent("C", "D"), 
parent("AA", "BB"),
parent("BB", "CC"),
ancestor("A", "B"), 
ancestor("B", "C"), 
ancestor("C", "D"), 
ancestor("AA", "BB"),
ancestor("BB", "CC")
ancestor("A", "C")
ancestor("B", "D")
ancestor("AA", "CC")
ancestor("A", "D")
# ----------------- New inferred facts below --------------


Aha! There are no more new inferred facts. If we do another pass on KnowledgeBase4, it would come out the same. So we can stop!

So the logic to stop would be:
Take the output of each iteration. If it matches the input stop(as we did not learn any new inferred facts). If not a match, then run another iteration. Let's call this method iterate_until_no_change

"""
def iterate_until_no_change(transform, initial_value):
    a_input = initial_value

    while True:
        a_output = transform(a_input)
        if a_output == a_input:
            return a_output
        a_input = a_output


"""
Now, we already have run_conjunction. That will be our transform function
"""

def run_recursive(database, rules, query):
    return _run_recursive(evaluate_rule_with_conjunction, query_variable_match, database, rules, query)


# TODO: Do we have to refactor _run_simple as well as it has some common parts with _run_recursive
def generate_knowledgebase(rules_evaluator, database, rules):
    result = database 
    for rule in rules:
        evaluation = rules_evaluator(rule, database)
        result = result.union(evaluation)
    return result 

    
def _run_recursive(rules_evaluator, match, database, rules, query):
    tranformer = lambda a_knowledgebase: generate_knowledgebase(rules_evaluator, a_knowledgebase, rules)
    knowledgebase = iterate_until_no_change(tranformer, database)
    return filter_facts(knowledgebase, query, match)

"""
Let's define the query
"""
query = ancestor(X, Y)

# recursive_result = run_recursive(database, rules, query)

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

# assert recursive_result == expected_result, f"{recursive_result} not equal to {expected_result}"

"""
Let's explore other queries we can ask.
Is AA the ancestor of C(No)

"""
# query = ancestor("AA", "C")

# assert run_recursive(database, rules, query) == set()

"""
What if I want to find all ancestors of C
"""
# query = ancestor(X, "C")
# assert run_recursive(database, rules, query) == {ancestor("A", "C"), ancestor("B", "C")}


"""
Finally, who are the intermediates between A and D i.e. B and C
intermediate(Z, X, Y) <= ancestor(X, Z), ancestor(Z, Y)
"""
intermediate = lambda intermediate, start, end: Relation("intermediate", (intermediate, start, end) )
intermediate_head = intermediate(Z, X, Y)
intermediate_body = {ancestor(X, Z), ancestor(Z, Y)} 
intermediate_rule = Rule(intermediate_head, intermediate_body)

rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
# rules = [intermediate_rule]
query = intermediate(Z, "A", "D")

assert run_recursive(database, rules, query) == {intermediate("B", "A", "D"), intermediate("C", "A", "D")}



success_str = '==================================== All Tests Pass ==================================================' 
print('\x1b[6;30;42m' + success_str + '\x1b[0m')

"""

* SQL does support recursion. I just find Datalog has a cleaner syntax. RA: Cite SQL Recursion Example

"""