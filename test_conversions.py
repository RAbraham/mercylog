import pytest
from mercylog.types import relation, variables, _
from mercylog.core import query_variables
import pandas as pd
parent = relation("parent")
man = relation("man")
X, Y, Z = variables("X", "Y", "Z")

# def parent(father, son): return dict(father=father, son=son)
# database = [
#         parent("Abe", "Bob"),  # Abe is a parent of Bob
#         parent("Abby", "Bob"),
#         parent("Bob", "Carl"),
#         parent("Bob", "Connor"),
#         parent("Beatrice", "Carl"),
#     ]
# db_df = pd.DataFrame(database)
# def test_db_df():
#         print(db_df)
    # parents_carl = run(database, [], [parent(X, "Carl")])
    # assert_df(parents_carl, a_df({X: ["Bob", "Beatrice"]}))

def test_query_variables():
    query = [man(X)]
    assert query_variables(query) == {X}
    query = [parent(X, "Carl")]
    assert query_variables(query) == {X}
    query = [man(X), parent(X, Z), parent(Z, Y)]
    assert query_variables(query) == {X, Y, Z}
    query = [parent(X, _)]
    assert query_variables(query) == {X}
    # TODO: we have to check if vars is passed, it is a valid subset of the query?
    # TODO: What about don't care variable i.e. m._
