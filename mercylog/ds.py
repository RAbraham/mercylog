from toolz.curried import *
from typing import *

from mercylog.types import DataSource, Relation, Rule, relation
from mercylog.core import run_df as run_df, _
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


class SimpleDataSource(DataSource):
    def __init__(self, relations: List[Relation]):
        self.relations = relations
        super(SimpleDataSource, self).__init__()

    def __call__(self, *args, **kwargs):
        query, rules = split_rules_query(args)
        rs_df = run_df(run_abcdatalog, self.relations, rules, query)
        return df_ds(rs_df)



class DataFrameDataSource(DataSource):
    def __init__(self, dataframe: DF):
        self.dataframe = dataframe
        self.simple_ds = SimpleDataSource(df_to_relations(dataframe))

    def df(self) -> DF:
        return self.dataframe

    def __call__(self, *args, **kwargs):
        return self.simple_ds(*args, **kwargs)

    def row(self, *args, **kwargs):
        r = pipe(kwargs.items(),
                 )

        '''
        [k,v]
        if columns = [id, name, age, gender], then relation is _row(_, X, _, "M") for row(name=X, gender='M') 
        
        [("name", X), (gender, "M")]
        [(1, X), (3, "M")]
        [(0, _), (1, X), (2, _), (3, "M")]
        (_, X, _, "M")

        '''
        return _row(list(self.dataframe.columns), kwargs)


def _row(columns: List[str], vars_dict: Dict[str, Any]) -> Relation:
    vars = vars_dict.keys()
    r = []
    for c in columns:
        if c in vars:
            r.append(vars_dict[c])
        else:
            r.append(_)

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
    rules = [a for a in args[0] if isinstance(a, Rule)]
    query = [a for a in args[0] if isinstance(a, Relation)]
    return query, rules

def facts(relations: List[Relation]) -> DataSource:
    return SimpleDataSource(relations)

def df_ds(df: DF) -> DataFrameDataSource:
    return DataFrameDataSource(df)
# def df(df: DF) -> DataSource:
#     relations = df_to_relations(df)
#     return SimpleDataSource(relations)


if __name__ == '__main__':
    s = SimpleDataSource([11, 22])
    print(s())