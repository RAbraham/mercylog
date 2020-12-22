from typing import *
import pandas as pd
from mercylog.types import Relation, Variable, Rule, relation

# from fastcore.utils import *
from toolz.curried import *
from placeholder import _


def make_run(run_func: Callable) -> Callable:
    return curry(run, run_func)

group_by_position = compose_left(
    map(_.terms), map(enumerate), concat, groupby(0)  # 0th in tuple is the index
)


def facts_to_dict(facts, query_vars):
    r = pipe(
        facts,
        group_by_position,
        valmap(lambda t: list(pluck(1, t))),  # drop the index from the values
        keymap(lambda k: query_vars[k]), # replace the index with vars
    )
    return r


def run(
    run_func: Callable,
    database: List[Relation],
    rules: List[Rule],
    query: List[Relation],
    variables: List[Variable] = None,
) -> pd.DataFrame:

    assert isinstance(database, List)
    assert isinstance(query, List)
    head, query_vars = get_head(query, variables)

    m = head <= query

    _rules = rules + [m]
    facts = run_func(database, _rules, head)
    result = facts_to_dict(facts, query_vars)

    return pd.DataFrame(result)


def get_head(query, variables):
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
