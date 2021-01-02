import pytest
import pandas as pd
from pprint import pprint
from mercylog.db import df_to_relations, _row, prow
from mercylog.types import relation, _
# _rows = relation("_rows")
_rows = prow
Abe = "Abe"
M = "M"
Bob = "Bob"
Abby = "Abby"
F = "F"

def test_df_to_relations():
    rows = [
        ["Abe", "M"],
        ["Bob", "M"],
        ["Abby", "F"]
    ]
    a_df = pd.DataFrame(rows, columns=["name", "gender"])
    exp = [_rows(Abe, M), _rows(Bob, M), _rows(Abby, F)]
    assert df_to_relations(a_df) == exp

def test_row():
    columns = ["id", "name", "age", "gender"]
    vars = dict(name="X", gender="M")
    assert _row(columns, vars) == prow(_, "X", _, "M")



#
# def test_dataframe():
#     test_df = to_df(facts)
#     db = DataFrameDataSource(test_df)
#     assert_df(db(query), exp)
#     pass

# test empty dataframe input and output