from typing import *
from dataclasses import dataclass
from pprint import pprint

"""
Let's start with a simple Datalog Program. 

man("Brad")
man("Abe")
person(X) :- man(X) # If someone is a man, then he is a person.

`person(X) :- man(X)` is called a rule.

`man` is like a table in a database. `man("Bob")` is a relation in that table. We'll call it a `base` relation i.e. a simple `fact`

`person(X)` is a derived relation, as it is derived from some base relation `man(X)`, similar to a view in the database.

X is a logical variable. It is used to refer to values abstractly. So man(X) could be used to abstractly refer to all man relations. 
"""


"""
we can create a logical variable like this:
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
`man(X)` or `person(X)` in `person(X) :- man(X)`

So a relation has a name(e.g. `parent`) and a list of attributes(e.g. "John" and "Chester" or X). 
"""

@dataclass(frozen=True, eq=True)
class Relation:
    """
    man("Bob) is Relation("man", ("Bob",)) # ("Bob",) is a single valued tuple
    parent("John", "Chester") is Relation("parent", ("John", "Chester"))
    man(X) is Relation("man", (Variable("X"),))

    """
    name: str
    attributes: Tuple 

"""
A rule could be:
- person(X) :- man(X) i.e. X is a person if he is man.
- father(X, Y) :- man(X), parent(X, Y) i.e. X is a father of Y if X is a man and X is the parent of Y

A rule has:
- a head relation which is on the left of the `:-` symbol e.g. person(X) and father(X, Y) above
- a body of relations which is on the right of the `:-` symbol e.g. man(X) and man(X), parent(X, Y) above

Since Datalog is declarative, the order of the relations in the body does not matter. Both the statements below have the same meaning:
father(X, Y) :- man(X), parent(X, Y) 
father(X, Y) :- parent(X, Y), man(X) # reversing the order does not matter

So, the body can be represented as a set

"""
@dataclass(frozen=True, eq=True)
class Rule:
    head: Relation
    body: Set[Relation]

"""
The last element of Datalog is the query. The simplest query is no rules, just facts. Given:
man("Abe)
man("Bob")
woman("Abby")

A query could be:
man(X) # Find me all men 

The query should return:
[man("Bob"), man("George")]

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
For some function `run_simplest`, I expect:
assert run_simplest(database, no_rules, query) == {abe, bob}
"""

"""
The simplest run would iterate through all the facts and filter those facts those which match the query by relation name.
"""

def name_match(fact: Relation, query: Relation) -> bool:
    return fact.name == query.name

def filter_facts(database: Set[Relation], query: Relation, match: Callable) -> Set[Relation]:
    return {fact for fact in database if match(fact, query)}

def run_simplest(database: Set[Relation], rules: List[Rule], query: Relation) -> Set[Relation]:
    return filter_facts(database, query, name_match) 

assert run_simplest(database, no_rules, query) == {abe, bob}

"""
Let's add some facts of length two 
parent("Abe", "Bob") # Abe is a parent of Bob
parent("Abby", "Bob")
parent("Bob", "Carl")
parent("Bob", "Connor")
parent("Beatrice", "Carl")

I may want to query who are the parents of Carl
Query:
parent(X, "Carl") # Should return {parent("Bob", "Carl"), parent("Beatrice", "Carl")}

parent(X, "Carl") is similar to `select * from parent where child = "Carl"` if there was a table parent with columns `parent` and `child`)


The beauty of Datalog is that you can ask the inverse without additional code e.g. Who are the children of Bob
parent("Bob", X) # Should return {parent("Bob", "Carl"), parent("Bob", "Connor")}

"""

"""
Let's code that up. Also from now on, I'm going to make a helper function to make it easy to express relations
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
For an enhanced function `run_with_filter`, we should have:
parents_carl =  run_with_filter(database, [], parent(X, "Carl")) 
assert parents_carl == {parent("Bob", "Carl"), parent("Beatrice", "Carl")}

children_bob =  run_with_filter(database, [], parent("Bob", X)) 
assert children_bob == {parent("Bob", "Carl"), parent("Bob", "Connor")}

"""

"""
Now, to the implementation. For a query to match, an argument at position N in the query should match the argument at position N in the fact.
"""

def query_variable_match(fact: Relation, query: Relation) -> bool:
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

def run_with_filter(database: Set[Relation], rules: List[Rule], query: Relation) -> Set[Relation]:
    return filter_facts(database, query, query_variable_match)

parents_carl =  run_with_filter(database, [], parent(X, "Carl")) 
assert parents_carl == {parent("Bob", "Carl"), parent("Beatrice", "Carl")}

children_bob =  run_with_filter(database, [], parent("Bob", X)) 
assert children_bob == {parent("Bob", "Carl"), parent("Bob", "Connor")}


"""
Let's add a rule to our program
man("Bob")
man("George")
animal("Tiger")
human(X) :- man(X) # You are human if you are man.

Query:
human(X) # Find me all humans

The query should return:
Ans: {human("Bob"), human("George")}

"""
man = lambda x: Relation("man", (x,))
animal = lambda x: Relation("animal", (x,))
human = lambda x: Relation("human", (x,))
X = Variable("X")

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

"""
For each rule, for each relation in it's body, if it matches with any of the facts in the database,
then get the attributes of that fact and transfer it to the head.
"""

def match_relation_and_fact(relation: Relation, fact: Relation) -> Optional[Dict]:
    if relation.name == fact.name:
        return dict(zip(relation.attributes, fact.attributes))

def match_relation_and_database(database: Set[Relation], relation: Relation) -> List[Dict]:
    inferred_attributes = []
    for fact in database:
        attributes = match_relation_and_fact(relation, fact)
        if attributes:
            inferred_attributes.append(attributes)
    return inferred_attributes


def evaluate_rule_simple(rule: Rule, database: Set[Relation]) -> Set[Relation]:
    relation = list(rule.body)[0] # For now, our body has only one relation
    all_matches = match_relation_and_database(database, relation)
    # We use the Python feature below that if we call `values` on a dictionary, it will preserve the order that was given when the dictionary was created i.e. in the `zip` inside `match_relation_and_database`. Thank God.
    return {Relation(rule.head.name, tuple(attributes.values())) for attributes in all_matches}

"""
This evaluate_rule_simple can be passed to a function which will `evaluate` it on each rule for the database to generate the final knowledge base.
"""
def generate_knowledgebase(evaluate: Callable, database: Set[Relation], rules: List[Rule]):
    knowledge_base = database 
    for rule in rules:
        evaluation = evaluate(rule, database)
        knowledge_base = knowledge_base.union(evaluation)
    return knowledge_base 

def run_rule_simple(database: Set[Relation], rules: List[Rule], query: Relation):
    knowledge_base = generate_knowledgebase(evaluate_rule_simple, database, rules)
    return filter_facts(knowledge_base, query, query_variable_match)

# Test Cases
simplest_rule_result = run_rule_simple(database, rules, query)
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
father(X, Y) :- parent(X, Y), man(X)

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
Similar as `run_rule_simple` but when we match the body to the facts, we have to check if the attributes match for the entire body,
"""
def run_logical_operators(database, rules, query):
    knowledge_base = generate_knowledgebase(evaluate_logical_operators_in_rule, database, rules)
    return filter_facts(knowledge_base, query, query_variable_match)

def evaluate_logical_operators_in_rule(rule: Rule, database: List[Relation]) -> Set[Relation]:
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
human(X) :- man(X)
human(X) :- woman(X)

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
ancestor(X, Y) :- parent(X, Y)
# If you are a parent of Y and Y is an an ancestor, then you are an ancestor as well.
ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)

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
# ancestor(X, Y) :- parent(X, Y)
ancestor_rule_base = Rule(ancestor(X, Y), [parent(X, Y)])
# ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)
ancestor_rule_recursive = Rule(ancestor(X, Z), {parent(X, Y), ancestor(Y, Z)})

rules = [ancestor_rule_base, ancestor_rule_recursive]

"""
Alright, let's dive into this. What is different from run_logical_operator? It's the hierarchy or recursion. If you see it as hierarchy(I'm visualizing this as a tree), one has to keep on going until we reach the top(or the bottom) of the tree. If we see it as a recursion, we keep on going till we hit the base case which terminates the recursion. So let's imagine how we would process the above example. In the first pass, we would do the simplest inference from base fact to derived fact using the base rule of ancestor(X, Y) :- parent(X, Y) 


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

Now that's done, we can focus on inference from a combination of inferred facts and base facts to new inferred facts using the recursive rule ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z). For e.g. in KnowledgeBase1, we have parent("C","D") and ancestor("B", "C") , so we can infer the fact ancestor("B", "D") i.e grandparents. We keep on doing this till we get:

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
Now, we already have run_logical_operator. That will be our transform function
"""

def run_recursive(database, rules, query):
    return _run_recursive(evaluate_logical_operators_in_rule, query_variable_match, database, rules, query)


    
def _run_recursive(rules_evaluator, match, database, rules, query):
    tranformer = lambda a_knowledgebase: generate_knowledgebase(rules_evaluator, a_knowledgebase, rules)
    knowledgebase = iterate_until_no_change(tranformer, database)
    return filter_facts(knowledgebase, query, match)

"""
Let's define the query
"""
query = ancestor(X, Y)

recursive_result = run_recursive(database, rules, query)

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

"""
Let's explore other queries we can ask.
Is AA the ancestor of C(No)

"""
query = ancestor("AA", "C")

assert run_recursive(database, rules, query) == set()

"""
What if I want to find all ancestors of C
"""
query = ancestor(X, "C")
assert run_recursive(database, rules, query) == {ancestor("A", "C"), ancestor("B", "C")}

"""
What if I want to find who all are the descendants of AA. The beauty of the Datalog query style is that I can use the same query but just reverse the order! 
"""
query = ancestor("AA", X)
assert run_recursive(database, rules, query) == {ancestor("AA", "BB"), ancestor("AA", "CC")}

"""
Finally, who are the intermediates between A and D i.e. B and C
Z is an intermediate of X and Y if X is it's ancestor and Y is its descendant
intermediate(Z, X, Y) :- ancestor(X, Z), ancestor(Z, Y)
"""
intermediate = lambda intermediate, start, end: Relation("intermediate", (intermediate, start, end) )
intermediate_head = intermediate(Z, X, Y)
intermediate_body = {ancestor(X, Z), ancestor(Z, Y)} 
intermediate_rule = Rule(intermediate_head, intermediate_body)

rules = [ancestor_rule_base, ancestor_rule_recursive, intermediate_rule]
query = intermediate(Z, "A", "D")

assert run_recursive(database, rules, query) == {intermediate("B", "A", "D"), intermediate("C", "A", "D")}


"""

* SQL does support recursion. I just find Datalog has a cleaner syntax. RA: Cite SQL Recursion Example
* One aspect of Datalog being declarative is that the order of rules does not matter either. So technically, instead of `rules = [rule1, rule2]`, we could have used `rules = frozenset([rule1, rule2])`. The latter is a bit more clutter so I used simple lists. Why `frozenset`? Because of [this](https://stackoverflow.com/questions/37105696/how-to-have-a-set-of-sets-in-python?lq=1)
"""

success_str = '==================================== All Tests Pass ==================================================' 
print('\x1b[6;30;42m' + success_str + '\x1b[0m')
