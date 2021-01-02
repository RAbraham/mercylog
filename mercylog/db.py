# from fastcore.dispatch import typedispatch
# from multimethod import multimethod
# from toolz.curried import *
from typing import *

from mercylog.types import Database, Relation, MercylogRule, relation, _ as m_
from mercylog.core import run_df as run_df
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
        return self.simple_ds(*args, **kwargs)

    def row(self, *args, **kwargs):
        # TODO: Assert kwargs are vars or constants. not relations for e.g.
        return _row(list(self.dataframe.columns), kwargs)


def _row(columns: List[str], vars_dict: Dict[str, Any]) -> Relation:
    vars = vars_dict.keys()
    r = []
    for c in columns:
        if c in vars:
            r.append(vars_dict[c])
        else:
            r.append(m_)

    return prow(*r)

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
    rules = [a for a in args[0] if isinstance(a, MercylogRule)]
    query = [a for a in args[0] if isinstance(a, Relation)]
    return query, rules



# @multimethod
def db(df: DF) -> DataFrameDB:
    return DataFrameDB(df)

# @multimethod
def facts(relations: List[Relation]) -> Database:
    return SimpleDB(relations)


if __name__ == '__main__':
    s = SimpleDB([11, 22])
    print(s())