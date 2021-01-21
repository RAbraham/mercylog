from mercylog.types import Variable
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Aggregate(ABC):

    def __init__(self):
        super().__init__()

    # @abstractmethod
    # def (self):
    #     pass

@dataclass(frozen=True)
class Count(Aggregate):
    variable: Variable

def count_(variable: Variable) -> Count:
    return Count(variable)
