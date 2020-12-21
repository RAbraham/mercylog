import pandas as pd
def a_df(a_dict):
    result =  pd.DataFrame(a_dict)
    return result

def assert_df(df1, df2):
    df1_dicts = df1.to_dict("records")
    df2_dicts = df2.to_dict("records")
    for item in df1_dicts:
        if item not in df2_dicts:
            assert False, f"{item} not in df2"
    for item in df2_dicts:
        if item not in df1_dicts:
            assert False, f"{item} not in df1"
