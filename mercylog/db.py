from typing import *
from mercylog.types import DataSource, Relation, Rule, relation
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



class SimpleDataSource(DataSource):
    def __init__(self, relations: List[Relation]):
        self.relations = relations
        super(SimpleDataSource, self).__init__()

    def __call__(self, *args, **kwargs):
        query, rules = split_rules_query(args)
        rs_df = run_df(run_abcdatalog, self.relations, rules, query)
        return df(rs_df)



class DataFrameDataSource(DataSource):
    def __init__(self, dataframe: DF):
        self.dataframe = dataframe
        self.simple_ds = SimpleDataSource(df_to_relations(dataframe))

    def df(self) -> DF:
        return self.dataframe

    def __call__(self, *args, **kwargs):
        return self.simple_ds(*args, **kwargs)

def df_to_relations(a_df: pd.DataFrame) -> List[Relation]:
    rel = relation("_rows")

    pass

def split_rules_query(args):
    rules = [a for a in args[0] if isinstance(a, Rule)]
    query = [a for a in args[0] if isinstance(a, Relation)]
    return query, rules

def facts(relations: List[Relation]) -> DataSource:
    return SimpleDataSource(relations)

def df(df: DF) -> DataFrameDataSource:
    return DataFrameDataSource(df)
# def df(df: DF) -> DataSource:
#     relations = df_to_relations(df)
#     return SimpleDataSource(relations)


if __name__ == '__main__':
    s = SimpleDataSource([11, 22])
    print(s())