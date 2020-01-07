from abc import abstractmethod, ABC
from typing import TypeVar

from asgiref.sync import sync_to_async


class Runnable(ABC):
    T = TypeVar('T')

    @classmethod
    async def run_async(cls, *args, **kwargs) -> T:
        return await sync_to_async(cls.run)(*args, **kwargs)

    @classmethod
    @abstractmethod
    def run(cls, *args, **kwargs) -> T: ...
