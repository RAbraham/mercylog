from typing import *
from dataclasses import dataclass
from mercylog.types import Variable, Relation, Rule


def filter_facts(database: Set[Relation], query: Relation, match: Callable) -> Set[Relation]:
    return {fact for fact in database if match(fact, query)}

def query_variable_match(fact: Relation, query: Relation) -> bool:
    if fact.name != query.name:
        return False

    # TODO: zip is duplicated?
    for query_term, fact_term in zip(query.terms, fact.terms):
        if not isinstance(query_term, Variable) and query_term != fact_term:
                return False
    return True  

def match_relation_and_fact(relation: Relation, fact: Relation) -> Optional[Dict]:
    if relation.name == fact.name:
        return dict(zip(relation.terms, fact.terms))

def match_relation_and_database(database: Set[Relation], relation: Relation) -> List[Dict]:
    inferred_terms = []
    for fact in database:
        terms = match_relation_and_fact(relation, fact)
        if terms:
            inferred_terms.append(terms)
    return inferred_terms


def generate_knowledgebase(evaluate: Callable, database: Set[Relation], rules: List[Rule]):
    knowledge_base = database 
    for rule in rules:
        evaluation = evaluate(rule, database)
        knowledge_base = knowledge_base.union(evaluation)
    return knowledge_base 

def has_common_value(attrs1: Dict[Variable, Any], attrs2: Dict[Variable, Any]) -> bool:
    common_vars = set(attrs1.keys()).intersection(set(attrs2.keys()))
    return all([attrs1[c] == attrs2[c] for c in common_vars])


def conjunct(body_terms: List[List[Dict]]) -> List:
    # TODO: Does not cover body lengths greater than 2
    result = []
    if len(body_terms) == 1:
        return body_terms[0]
    
    attr1 = body_terms[0]
    attr2 = body_terms[1]
    for a1 in attr1:
        for a2 in attr2:
            _c = has_common_value(a1, a2)
            if _c:
                result.append({**a1, **a2})
    return result

def rule_terms(relation: Relation, attr: Dict[Variable, Any]) -> Tuple:
    return tuple([attr[a] for a in relation.terms])


def evaluate_logical_operators_in_rule(rule: Rule, database: List[Relation]) -> Set[Relation]:
    body_terms = []

    for relation in rule.body:
        _terms = match_relation_and_database(database, relation)
        body_terms.append(_terms)

    terms = conjunct(body_terms)
    
    return {Relation(rule.head.name, rule_terms(rule.head, attr)) for attr in terms}

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
