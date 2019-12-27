from abc import abstractmethod, ABC


class Runnable(ABC):
    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> object: ...
