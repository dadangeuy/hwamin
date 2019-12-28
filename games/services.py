import ast
import operator
from typing import Tuple

from factory.fuzzy import FuzzyInteger
from simpleeval import SimpleEval

from commons.patterns import Runnable


class DuaEmpatQuestionGeneratorService(Runnable):
    FUZZY_INTEGER = FuzzyInteger(low=1, high=13)

    @classmethod
    def run(cls) -> Tuple[int, int, int, int]:
        return (
            cls._get_random_int(),
            cls._get_random_int(),
            cls._get_random_int(),
            cls._get_random_int()
        )

    @classmethod
    def _get_random_int(cls) -> int:
        return cls.FUZZY_INTEGER.fuzz()


class DuaEmpatCalculatorService(Runnable):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }
    EVAL = SimpleEval(operators=OPERATORS)

    @classmethod
    def run(cls, text: str) -> bool:
        return cls.EVAL.eval(text)
