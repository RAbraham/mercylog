from typing import *
from types import DataSource, Relation, Result, Program, KnowledgeBase

def query(data_source: DataSource, program: List[Relation], query: List[Relation]):
    _f = fixpoint(data_source, Program(program + query))

def fixpoint(data_source: DataSource, program: Program, immediate_consequence: Callable) -> Result:
    _previous = KnowledgeBase()
    while True:
        _current = immediate_consequence(data_source, _previous)
        if _previous == _current:
            break
    
    return Result(_current)

def immediate_consequence(data_source, knowledge_base) -> Result:
    pass