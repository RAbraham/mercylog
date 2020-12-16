from typing import *
import toolz
from functools import partial
from mercylog.abcdatalog.engine.bottomup.bottom_up_engine_frame import BottomUpEngineFrame
from mercylog.abcdatalog.engine.bottomup.sequential.semi_naive_eval_manager import SemiNaiveEvalManager
from mercylog.types import Rule, relation, variables
from mercylog.abcdatalog.engine.datalog_engine import DatalogEngine
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import convert, q as do_query


p = relation("p")
q = relation("q")
r = relation("r")
s = relation("s")

V, W, X, Y, Z = variables("V", "W", "X", "Y", "Z")


def seminaive_engine():
    return BottomUpEngineFrame(SemiNaiveEvalManager())


def initEngine_engine(engine: DatalogEngine, program: List[Rule]):
    converted = convert(list(program))
    engine.init(converted)
    return engine



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
def match(program, query, result):
    semi_engine = seminaive_engine()
    initEngine = partial(initEngine_engine, semi_engine)
    engine = initEngine(program)
    return is_result(engine, query, result)

