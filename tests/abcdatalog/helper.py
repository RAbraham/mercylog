from typing import *

from mercylog.abcdatalog.engine.bottomup.bottom_up_engine_frame import BottomUpEngineFrame
from mercylog.abcdatalog.engine.bottomup.sequential.semi_naive_eval_manager import SemiNaiveEvalManager
from mercylog.types import Rule
from mercylog.abcdatalog.engine.datalog_engine import DatalogEngine
from mercylog.abcdatalog.ast.mercylog_to_abcdatalog import convert

def seminaive_engine():
    return BottomUpEngineFrame(SemiNaiveEvalManager())

def initEngine_engine(engine: DatalogEngine, program: List[Rule]):
    converted = convert(list(program))
    engine.init(converted)
    return engine
