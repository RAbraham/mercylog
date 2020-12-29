import pytest
import pandas as pd
# from mercylog import df
def test_user_api():
    #     df = pd.DataFrame(r, columns=["var", "value"])
    rows = [
        ["Abe", "M"],
        ["Bob", "M"],
        ["Abby", "F"]
    ]
    a_df = pd.DataFrame(rows, columns=["name", "gender"])
    # print(">> Name")
    # a_df.name = "person"
    # print(a_df.name)
    # select males
    # db = df(a_df)
    # males = db([
    #
    # ])



    pass