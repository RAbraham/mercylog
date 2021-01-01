import pytest
import pandas as pd
from mercylog import df_ds,  R, V
from tests.abcdatalog.helper import assert_df

# API
# ds = df(customer_df) # with many columns
# ds([
#     R.customer(Id, Name, Age) <= ds.row(customer_id=Id, name=Name, age=Age)
#     R.customer(Id, _,  Age) # R.customer(Id=Id, Age=Age) # or R.customer({Id, Age})
# ])


def test_user_api_filter():
    X = V.X
    rows = [["Abe", "M"], ["Bob", "M"], ["Abby", "F"]]
    a_df = pd.DataFrame(rows, columns=["name", "gender"])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=[X])

    ds = df_ds(a_df)
    # select males
    males = ds([ds.row(name=X, gender="M")])
    assert_df(males.df(), exp_df)


def test_single_body_rule():
    X = V.X
    rows = [["Abe", "man"], ["Bob", "man"], ["Samba", "animal"]]
    a_df = pd.DataFrame(rows, columns=["name", "species"])
    exp_df = pd.DataFrame(["Abe", "Bob"], columns=[X])

    # Then
    ds = df_ds(a_df)
    man = R.man(X) <= ds.row(name=X, species="man")
    human = ds([man, R.man(X)])

    assert_df(human.df(), exp_df)
