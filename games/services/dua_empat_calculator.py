import ast
import operator
import re
from typing import Iterable

from simpleeval import SimpleEval

from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable


class DuaEmpatCalculatorService(Runnable):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }
    EVAL = SimpleEval(operators=OPERATORS)

    @classmethod
    def run(cls, numbers: Iterable[int], text: str) -> bool:
        cls._validate(numbers, text)
        return cls.EVAL.eval(text)

    @classmethod
    def _validate(cls, numbers: Iterable[int], text: str) -> None:
        cls._validate_formula(text)
        cls._validate_numbers(numbers, text)

    @staticmethod
    def _validate_formula(text: str):
        non_formula_text = re.search(r'[^ ()*+\-/0-9]', text)
        if non_formula_text is not None:
            raise UnknownCommandException

    @staticmethod
    def _validate_numbers(numbers: Iterable[int], text: str):
        text_numbers = re.split(r'[^0-9]', text)
        text_numbers = filter(None, text_numbers)
        text_numbers = (int(text) for text in text_numbers)
        numbers = sorted(numbers)
        text_numbers = sorted(text_numbers)
        if numbers != text_numbers:
            raise UnknownCommandException
