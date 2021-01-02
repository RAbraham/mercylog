# from typing import *
# from mercylog.types import Variable, Relation, MercylogRule,  relation
# import pandas as pd
#
#
# def filter_facts(
#     database: List[Relation], query: Relation, match: Callable
# ) -> List[Relation]:
#     return [fact for fact in database if match(fact, query)]
#
#
# def query_variable_match(fact: Relation, query: Relation) -> bool:
#     if fact.name != query.name:
#         return False
#
#     # TODO: zip is duplicated?
#     for query_term, fact_term in zip(query.terms, fact.terms):
#         if not isinstance(query_term, Variable) and query_term != fact_term:
#             return False
#     return True
#
#
# def match_relation_and_fact(relation: Relation, fact: Relation) -> Optional[Dict]:
#     if relation.name == fact.name:
#         zipped = zip(relation.terms, fact.terms)
#         for rt, ft in zipped:
#             if not isinstance(rt, Variable) and rt != ft:
#                 return None
#         return dict(zip(relation.terms, fact.terms))
#
#
# def match_relation_and_database(
#     database: List[Relation], relation: Relation
# ) -> List[Dict]:
#     inferred_terms = []
#     for fact in database:
#         terms = match_relation_and_fact(relation, fact)
#         if terms:
#             inferred_terms.append(terms)
#     return inferred_terms
#
#
# def generate_knowledgebase(
#     evaluate: Callable, database: Set[Relation], rules: List[MercylogRule]
# ):
#     knowledge_base = database
#     for rule in rules:
#         evaluation = evaluate(rule, database)
#         knowledge_base = set(knowledge_base).union(set(evaluation))
#     return knowledge_base
#
#
# def has_common_value(attrs1: Dict[Variable, Any], attrs2: Dict[Variable, Any]) -> bool:
#     common_vars = set(attrs1.keys()).intersection(set(attrs2.keys()))
#     return all([attrs1[c] == attrs2[c] for c in common_vars])
#
#
# def _conjunct(a, b):
#     result = []
#     for a1 in a:
#         for a2 in b:
#             _c = has_common_value(a1, a2)
#             if _c:
#                 result.append({**a1, **a2})
#     return result
#
#
# def conjunct(body_terms: List[List[Dict]]) -> List:
#     if not body_terms:
#         return []
#     r = body_terms[0]
#     for _b in body_terms[1:]:
#         r = _conjunct(r, _b)
#
#     return r
#
#
# def rule_terms(relation: Relation, attr: Dict[Variable, Any]) -> Tuple:
#     return tuple([attr[a] for a in relation.terms])
#
#
# def evaluate_logical_operators_in_rule(
#     rule: Rule, database: List[Relation]
# ) -> List[Relation]:
#     body_terms = []
#
#     for relation in rule.body:
#         _terms = match_relation_and_database(database, relation)
#         body_terms.append(_terms)
#
#     terms = conjunct(body_terms)
#
#     return list(
#         {Relation(rule.head.name, rule_terms(rule.head, attr)) for attr in terms}
#     )
#
#
# def iterate_until_no_change(transform: Callable, initial_value: List) -> List:
#     a_input = initial_value
#
#     while True:
#         a_output = transform(a_input)
#         if a_output == a_input:
#             return a_output
#         a_input = a_output
#
#
# def run_simple(database,_rules, head):
#     transformer = lambda a_knowledgebase: generate_knowledgebase(
#         evaluate_logical_operators_in_rule, a_knowledgebase, _rules
#     )
#     knowledgebase = iterate_until_no_change(transformer, database)
#     facts = filter_facts(knowledgebase, head, query_variable_match)
#     return facts
#
#
