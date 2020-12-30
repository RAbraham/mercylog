import pytest
import pandas as pd
from mercylog import df, relation, _, Variable
from tests.abcdatalog.helper import assert_df
def test_user_api():
    rows = [
        ["Abe", "M"],
        ["Bob", "M"],
        ["Abby", "F"]
    ]
    _rows = relation("_rows")
    X = Variable("X")
    a_df = pd.DataFrame(rows, columns=["name", "gender"])
    # select males
    ds = df(a_df)
    males = ds([_rows(X, "M")])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=[X])
    assert_df(males.df(), exp_df)

    print(males.df())





