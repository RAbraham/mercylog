from typing import *
import pandas as pd
from mercylog.types import Relation, Variable, Rule, relation

# from fastcore.utils import *
from toolz.curried import *
from placeholder import _


def make_run(run_func: Callable) -> Callable:
    return curry(run_df, run_func)


group_by_position = compose_left(
    map(enumerate), concat, groupby(0)  # 0th in tuple is the index
)
# group_relation_terms_by_position = compose_left(group_by_position)


# def facts_to_dict(facts, query_vars):
#     r = pipe(
#         facts,
#         map(_.terms),
#         group_by_position,
#         valmap(lambda t: list(pluck(1, t))),  # drop the index from the values
#         keymap(lambda k: query_vars[k]),  # replace the index with vars
#     )
#     return r


def list_to_dict(a_list, query_vars):
    return pipe(
        a_list,
        group_by_position,
        valmap(lambda t: list(pluck(1, t))),  # drop the index from the values
        keymap(lambda k: query_vars[k]),  # replace the index with vars
    )




def facts_to_dict(facts, query_vars):
    r = pipe(facts, map(_.terms))

    return list_to_dict(r, query_vars)

# def facts_to_dict(facts, query_vars):
#     r = pipe(facts, map(_.terms), map(enumerate), concat,
#              map(lambda t: (query_vars[t[0]], t[1])))
#     from siuba import group_by as s_group_by, summarize, _ as s_
#     df = pd.DataFrame(r, columns=["var", "value"])
#     print(">> RA: Facts To Dict")
#     grouped = df >> s_group_by(s_.var)
#     result = grouped >> summarize(values= [s_.value.tolist()])
#     print(result)
#     return result
#
#     '''
#        var value
# 0    X     a
# 1    Y     c
# 2    X     c
# 3    Y     d
# 4    X     b
# 5    Y     c
# 6    X     a
# 7    Y     b
# 8    X     b
# 9    Y     d
# 10   X     a
# 11   Y     d
#
#     '''
#


    # return list_to_dict(r, query_vars)

def run_df(
    run_func: Callable,
    database: List[Relation],
    rules: List[Rule],
    query: List[Relation],
    variables: List[Variable] = None,
) -> pd.DataFrame:

    facts, query_vars = run_relations(database, query, rules, run_func, variables)
    return relations_to_df(facts, query_vars)


def relations_to_df(facts, query_vars):
    result = facts_to_dict(facts, query_vars)
    return pd.DataFrame(result)


def run_relations(database, query, rules, run_func, variables=None):
    # assert isinstance(database, List)
    assert isinstance(query, List)
    head, query_vars = get_head(query, variables)
    m = head <= query
    _rules = rules + [m]
    facts = run_func(database, _rules, head)
    return facts, query_vars


def get_head(query, variables=None):
    main_query_rule = relation("main_query_rule")
    query_vars = variables or list(query_variables(query))
    head = main_query_rule(*query_vars)
    return head, query_vars


def query_variables(query: List[Relation]) -> Set[Variable]:
    from placeholder import m

    r = pipe(
        query,
        map(m.variables()),
        concat,
        filter(lambda v: str(v) != "_" and isinstance(v, Variable)),
        set,

    )
    return r

def query_variables_list(query: List[Relation]) -> List[Variable]:
    from placeholder import m

    r = pipe(
        query,
        map(m.variables()),
        concat,
        filter(lambda v: str(v) != "_" and isinstance(v, Variable)),
        unique,
        list
    )
    return r
