import pytest
import pandas as pd
from mercylog import db, R, V, or_, and_, eq
from mercylog.df import row
from tests.abcdatalog.helper import assert_df
from mercylog import aggregates as a

from tests.util import assert_df, a_df

PEOPLE_COLUMNS = ["name", "name2", "rel"]

_parent = lambda parent, child: [parent, child, "parent"]
X = V.X
Y = V.Y
Z = V.Z

def test_count():
    """
    reachable(X,Y) :- link(X,Y).reachable(X,Y) :- reachable(X,Z), link(Z,Y).summary(X, count<Y>) :- reachable(X,Y).

    """
    reachable = R.reachable
    link = R.link
    summary = R.summary
    rules = [
        reachable(X, Y) << link(X, Y),
        reachable(X, Y) << and_(reachable(X, Z), link(Z, Y)),
        summary(X, a.count_(Y)) << reachable(X, Y)

    ]
    pass

def test_accumulator():
    """
		path(X,Y,[X,Y],C) :- link(X,Y,C).
		path(X,Y,P,C) :- path(X,Z,P1,C1), link(Z,Y,C2), P = [P1,Y], C = C1 + C2.
		shortest_path_len(X,Y,min<C>) :- path(X,Y,P,C).
		shortest_path(X,Y,P,C) :- shortest_path_len(X,Y,C), path(X,Y,P,C).
    """

    pass
