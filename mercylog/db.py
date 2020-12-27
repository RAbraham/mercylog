from typing import *
from mercylog.types import DataSource, Relation, Rule
from mercylog.core import run as run_df
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import (
    q as do_query,
    run_abcdatalog,
    initEngine_engine,
    seminaive_engine,
)
def facts(relations: List[Relation]) -> DataSource:
    return SimpleDataSource(relations)


class SimpleDataSource(DataSource):
    def __init__(self, relations: List[Relation]):
        self.relations = relations
        super(SimpleDataSource, self).__init__()

    def __call__(self, *args, **kwargs):
        # rules = list(filter(lambda a: isinstance(a, Rule), args[0]))
        rules = [a for a in args[0] if isinstance(a, Rule)]
        # query = filter(lambda a: isinstance(a, Relation), args[0])
        query = [a for a in args[0] if isinstance(a, Relation)]
        rs_df = run_df(run_abcdatalog, self.relations, rules, query)
        return rs_df

if __name__ == '__main__':
    s = SimpleDataSource([11, 22])
    print(s())