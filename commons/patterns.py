from abc import abstractmethod, ABC
from typing import TypeVar


class Runnable(ABC):
    T = TypeVar('T')

    @classmethod
    async def run_async(cls, **kwargs) -> T:
        return cls.run(**kwargs)

    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> T: ...
