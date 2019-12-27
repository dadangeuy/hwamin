from abc import abstractmethod, ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class Runnable(ABC, Generic[T]):
    @classmethod
    async def run_async(cls, **kwargs) -> T: return cls.run(**kwargs)

    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> T: ...
