from typing import *
import pandas as pd
from mercylog.types import Relation, Variable, Rule, relation
from fastcore.utils import *
from toolz.curried import *


def make_run(run_func: Callable) -> Callable:
    return toolz.curry(run, run_func)


def facts_to_dict(facts, query_vars):
    result = {}
    for ix, variable in enumerate(query_vars):
        result[variable] = []
        for f in facts:
            result[variable].append(f.terms[ix])
        result[variable] = result[variable]
    return result


def run(
    run_func: Callable,
    database: List[Relation],
    rules: List[Rule],
    query: List[Relation],
    variables: List[Variable] = None,
) -> pd.DataFrame:

    assert isinstance(database, List)
    assert isinstance(query, List)
    main_query_rule = relation("main_query_rule")

    query_vars = variables or list(query_variables(query))
    head = main_query_rule(*query_vars)
    m = head <= query

    _rules = rules + [m]
    facts = run_func(database, _rules, head)
    result = facts_to_dict(facts, query_vars)

    return pd.DataFrame(result)


def query_variables(query: List[Relation]) -> Set[Variable]:
    r = pipe(
        query,
        map(Self.variables()),
        concat,
        filter(lambda v: str(v) != "_" and isinstance(v, Variable)),
        set
    )
    return r
