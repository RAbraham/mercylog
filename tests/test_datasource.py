import pytest
import pandas as pd
from pprint import pprint
from mercylog.ds import df_to_relations
from mercylog.types import relation
_rows = relation("_rows")
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
#
# def test_dataframe():
#     test_df = to_df(facts)
#     db = DataFrameDataSource(test_df)
#     assert_df(db(query), exp)
#     pass

# test empty dataframe input and output