from typing import *
from dataclasses import dataclass
from pprint import pprint

@dataclass(frozen=True)
class Variable:
    name: str

@dataclass(frozen=True, eq=True)
class Relation:
    """
    man("Bob) is Relation("man", ("Bob",)) # ("Bob",) is a single valued tuple
    parent("John", "Chester") is Relation("parent", ("John", "Chester"))
    man(X) is Relation("man", (Variable("X"),))

    """
    name: str
    attributes: Tuple

@dataclass(frozen=True, eq=True)
class Rule:
    head: Relation
    body: Set[Relation]

def filter_facts(database: Set[Relation], query: Relation, match: Callable) -> Set[Relation]:
    return {fact for fact in database if match(fact, query)}

def query_variable_match(fact: Relation, query: Relation) -> bool:
    if fact.name != query.name:
        return False

    # TODO: zip is duplicated?
    for query_attribute, fact_attribute in zip(query.attributes, fact.attributes):
        if not isinstance(query_attribute, Variable) and query_attribute != fact_attribute:
                return False
    return True  

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


def generate_knowledgebase(evaluate: Callable, database: Set[Relation], rules: List[Rule]):
    knowledge_base = database 
    for rule in rules:
        evaluation = evaluate(rule, database)
        knowledge_base = knowledge_base.union(evaluation)
    return knowledge_base 

def has_common_value(attrs1: Dict[Variable, Any], attrs2: Dict[Variable, Any]) -> bool:
    common_vars = set(attrs1.keys()).intersection(set(attrs2.keys()))
    return all([attrs1[c] == attrs2[c] for c in common_vars])


def conjunct(body_attributes: List[List[Dict]]) -> List:
    # TODO: Does not cover body lengths greater than 2
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

def rule_attributes(relation: Relation, attr: Dict[Variable, Any]) -> Tuple:
    return tuple([attr[a] for a in relation.attributes])


def evaluate_logical_operators_in_rule(rule: Rule, database: List[Relation]) -> Set[Relation]:
    body_attributes = []

    for relation in rule.body:
        _attributes = match_relation_and_database(database, relation)
        body_attributes.append(_attributes)

    attributes = conjunct(body_attributes)
    
    return {Relation(rule.head.name, rule_attributes(rule.head, attr)) for attr in attributes}

def run_logical_operators(database: Set[Relation], rules: List[Rule], query: Relation):
    knowledge_base = generate_knowledgebase(evaluate_logical_operators_in_rule, database, rules)
    return filter_facts(knowledge_base, query, query_variable_match)


def iterate_until_no_change(transform: Callable, initial_value: Set) -> Set:
    a_input = initial_value

    while True:
        a_output = transform(a_input)
        if a_output == a_input:
            return a_output
        a_input = a_output

def run(database: Set[Relation], rules: List[Rule], query: Relation):
    transformer = lambda a_knowledgebase: generate_knowledgebase(evaluate_logical_operators_in_rule, a_knowledgebase, rules)
    knowledgebase = iterate_until_no_change(transformer, database)
    return filter_facts(knowledgebase, query, query_variable_match)
