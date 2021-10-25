# from fastcore.dispatch import typedispatch
# from multimethod import multimethod
from toolz.curried import *
from typing import *

from mercylog.lib.util import print_stop
from mercylog.types import (
    Database,
    Relation,
    MercylogRule,
    Variable,
    relation,
    _ as m_,
    Body,
    OrRelationGroup,
)
from mercylog.core import run_df as run_df, RowRelation

# from mercylog.core import run_relations, relations_to_df, run_df
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import (
    q as do_query,
    run_abcdatalog,
    initEngine_engine,
    seminaive_engine,
)
import pandas as pd

DF = pd.DataFrame

rel = relation("_row")
prow = rel


class SimpleDB(Database):
    def __init__(self, relations: List[Relation]):
        self.relations = relations
        super(SimpleDB, self).__init__()

    def __call__(self, *args, **kwargs):
        query, rules = split_rules_query(args)
        rs_df = run_df(run_abcdatalog, self.relations, rules, query)
        return db(rs_df)


class DataFrameDB(Database):
    def __init__(self, dataframe: DF):
        self.dataframe = dataframe
        self.simple_ds = SimpleDB(df_to_relations(dataframe))

    def df(self) -> DF:
        return self.dataframe

    def __call__(self, *args, **kwargs):
        _convert = convert_row(self.dataframe)
        clauses = [list(map(_convert, args[0]))]
        return self.simple_ds(*clauses, **kwargs)


def _row(columns: List[str], vars_dict: Dict[str, Any]) -> Relation:
    vars = vars_dict.keys()
    r = []
    for c in columns:
        if c in vars:
            r.append(vars_dict[c])
        else:
            r.append(m_)

    return prow(*r)


@curry
def convert_row(df, clause):
    if isinstance(clause, MercylogRule):
        body = body_to_relation(df, clause.body)
        return MercylogRule(clause.head, body)
    elif isinstance(clause, RowRelation):
        return row_to_relation(df, clause)
    else:
        return clause


def row_to_relation(df, clause):
    return _row(list(df.columns), clause.terms)


@curry
def body_to_relation(df, body: Body) -> Body:
    if isinstance(body, Relation):
        return body
    elif isinstance(body, RowRelation):
        return row_to_relation(df, body)
    elif isinstance(body, list):
        return [body_to_relation(df, b) for b in body]
    elif isinstance(body, OrRelationGroup):
        new_relations = [body_to_relation(df, b) for b in body.relations]
        return OrRelationGroup(new_relations)

    pass


def df_to_relations(a_df: pd.DataFrame) -> List[Relation]:
    c_list = []
    for c in a_df.columns:
        c_list.append(a_df[c])

    zipped = zip(*c_list)
    result = []
    for t in zipped:
        result.append(rel(*t))

    return result


def split_rules_query(args):
    rules = [a for a in args[0] if is_rule(a) or is_fact(a)]
    query = [a for a in args[0] if is_query(a)]
    return query, rules


# @multimethod
def db(df: Optional[DF] = None) -> DataFrameDB:
    if df is None:
        df = pd.DataFrame()

    return DataFrameDB(df)


# @multimethod
def facts(relations: List[Relation]) -> Database:
    return SimpleDB(relations)


def is_query(a: Relation) -> bool:
    return isinstance(a, Relation) and not is_rule(a) and not is_fact(a)


def is_rule(a: Relation) -> bool:
    return isinstance(a, MercylogRule)


def is_fact(a: Relation) -> bool:
    return not any(isinstance(t, Variable) for t in a.terms)


if __name__ == "__main__":
    s = SimpleDB([11, 22])
    print(s())
