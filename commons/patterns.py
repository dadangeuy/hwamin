from abc import abstractmethod, ABC
from typing import TypeVar, Generic

class Runnable(ABC):
    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> any: ...
