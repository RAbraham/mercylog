from typing import *
from mercylog.types import DataSource, Relation, Rule
from mercylog.core import run as run_df
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
        rules = [a for a in args[0] if isinstance(a, Rule)]
        query = [a for a in args[0] if isinstance(a, Relation)]
        rs_df = run_df(run_abcdatalog, self.relations, rules, query)
        return rs_df

class DataFrameDataSource(DataSource):
    def __init__(self, dataframe: DF):
        self.dataframe = dataframe

    def df(self) -> DF:
        return self.dataframe


def facts(relations: List[Relation]) -> DataSource:
    return SimpleDataSource(relations)

def df(df: DF) -> DataFrameDataSource:
    return DataFrameDataSource(df)

if __name__ == '__main__':
    s = SimpleDataSource([11, 22])
    print(s())