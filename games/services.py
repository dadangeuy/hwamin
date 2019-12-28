import ast
import operator
import re
from typing import Tuple, List

from factory.fuzzy import FuzzyInteger
from simpleeval import SimpleEval

from commons.patterns import Runnable


class DuaEmpatGeneratorService(Runnable):
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
    def run(cls, numbers: List[int], text: str) -> bool:
        cls._validate(numbers, text)
        return cls.EVAL.eval(text)

    @classmethod
    def _validate(cls, numbers: List[int], text: str) -> None:
        cls._validate_formula(text)
        cls._validate_numbers(numbers, text)

    @staticmethod
    def _validate_formula(text: str):
        non_formula_text = re.search(r'[^ ()*+\-/0-9]', text)
        if non_formula_text is not None:
            raise Exception

    @staticmethod
    def _validate_numbers(numbers: List[int], text: str):
        text_numbers = re.split(r'[^0-9]', text)
        text_numbers = filter(None, text_numbers)
        text_numbers = [int(text) for text in text_numbers]
        numbers = sorted(numbers)
        text_numbers = sorted(text_numbers)
        if numbers != text_numbers:
            raise Exception
