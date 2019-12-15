from abc import ABC, abstractmethod


class Runnable(ABC):
    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> any:
        pass
