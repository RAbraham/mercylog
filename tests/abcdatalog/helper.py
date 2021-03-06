from fastcore.utils import *
from pprint import pprint
from typing import *
import toolz
from toolz.curried import reduce as tzreduce
from toolz.curried import *

from functools import partial

from tests.util import assert_df, a_df
from mercylog.core import run_df as run_df, query_variables_list, list_to_dict
from mercylog.types import relation, variables, Relation
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import (
    q as do_query,
    run_abcdatalog,
    initEngine_engine,
    seminaive_engine,
)
import pandas as pd

NOT_TOKEN = "~"
p = relation("p")
q = relation("q")
r = relation("r")
s = relation("s")
a = "a"
b = "b"
c = "c"
d = "d"
e = "e"
tc = relation("tc")
not_tc = relation("not_tc")
edge = relation("edge")
node = relation("node")
cycle = relation("cycle")
noncycle = relation("noncycle")
beginsAtC = relation("beginsAtC")
beginsNotAtC = relation("beginsNotAtC ")
noC = relation("noC")

U, V, W, X, Y, Z = variables("U", "V", "W", "X", "Y", "Z")


@toolz.curry
def is_result(engine, a_query, exp_result):
    rs = do_query(engine, a_query)
    return _equals(rs, exp_result)


def list_set(a_list: List) -> List:
    result = []
    for a in a_list:
        if a not in result:
            result.append(a)
    return result


def _equals(act, exp):
    _act = list_set(act)
    _exp = list_set(exp)

    assert len(_act) == len(_exp), f"Act:{act} is not of same size as Exp:{exp}"
    for e in _exp:
        assert e in _act, f"Fact:{e} was not present in Actual:{act}"
    return True


@toolz.curry
def match_relations(program, query, result):
    """
    Keeping match though we have match1 because sometime we want to test zero arity relations.
    I don't want to remove it right now. We can't do that for match1 as we have to have some
    values in a dataframe.

    """
    semi_engine = seminaive_engine()
    initEngine = partial(initEngine_engine, semi_engine)
    engine = initEngine(program)
    return is_result(engine, query, result)


@toolz.curry
def match1(database, rules, query: Relation, result: Dict):
    rs_df = run_df(run_abcdatalog, database, rules, [query])
    return assert_df(rs_df, a_df(result))


@toolz.curry
def match3(database, rules, query: Relation, result: List[Tuple]):
    rs_df = database(rules + [query]).df()
    return assert_df(rs_df, _df(result, [query]))


def _df(facts: List[Tuple], query: List[Relation]):
    '''
    first, get the query vars.

    '''
    _vars = query_variables_list(query)
    return pd.DataFrame(list_to_dict(facts, _vars))

def strip_whitespace(p: str):
    import re

    return re.sub("[\s+]", "", p)


def parse_atom(atom: str) -> str:
    _result = ""
    _result = atom.split("(")
    if not atom:
        return ""
    if len(_result) == 1:
        result = _result[0] + "()"
    else:
        _terms = _result[1].split(")")[0].split(",")
        _terms = ", ".join(_terms)
        result = _result[0] + "(" + _terms + ")"
    return result


def parse_body(body: str) -> str:
    sp = body.split("),")
    if len(sp) == 1:
        return body
    else:
        return "[" + body + "]"


# def parse_clause(clauses) -> List:
#     result = []
#     for clause in clauses:
#         splitted = clause.split(":-")
#         head = splitted[0]
#         if len(splitted) == 1:
#             body = ""
#         else:
#             body = splitted[1]
#         parsed_head = parse_atom(head)
#         if body:
#             parsed_body = parse_body(body)
#             parsed_clause = " <= ".join([parsed_head, parsed_body])
#         else:
#             parsed_clause = parsed_head
#
#         result.append(parsed_clause)
#     return result


def parse_clause(clause) -> str:
    splitted = clause.split(":-")
    head = splitted[0]
    if len(splitted) == 1:
        body = ""
    else:
        body = splitted[1]
    parsed_head = parse_atom(head)
    if body:
        parsed_body = parse_body(body)
        parsed_clause = " <= ".join([parsed_head, parsed_body])
    else:
        parsed_clause = parsed_head
    return parsed_clause


def parse_clauses(clauses) -> List:
    return toolz.map(parse_clause, clauses)


def parse_nots(program: str) -> str:
    """
    We want to remove spaces but there is a space after not which should be kept. So we replace "note<space>" with "__mercylog__not_token__"
    which will be replaced by "not<space" after the general spaces are removed
    """
    return program.replace("not ", NOT_TOKEN)


def parse(program: str):
    from operator import add

    r = pipe(
        program,
        parse_nots,
        strip_whitespace,
        Self.split("."),
        map(parse_clause),
        interpose(",\n"),
        tzreduce(add),
    )

    result = r
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>> Parsed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(result)
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>> Parsed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    return result


if __name__ == "__main__":
    program = (
        "edge(a,b). edge(b,c). tc(a,c). tc(X,Y) :- edge(X,Y). tc(X,Y) :- tc(X,Z), tc(Z,Y)."
        + "node(X) :- edge(X,_). node(X) :- edge(_,X). not_tc(X,Y) :- node(X), node(Y), not tc(X,Y)."
    )

    # parse(program)
    act = (
        "edge(a, b),\n"
        "edge(b, c),\n"
        "tc(a, c),\n"
        "tc(X, Y) <= edge(X,Y),\n"
        "tc(X, Y) <= [tc(X,Z),tc(Z,Y)],\n"
        "node(X) <= edge(X,_),\n"
        "node(X) <= edge(_,X),\n"
        "not_tc(X, Y) <= [node(X),node(Y),~tc(X,Y)],\n"
    )
    assert parse(program) == act
