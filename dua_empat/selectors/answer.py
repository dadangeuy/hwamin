import ast
import operator
import re

from rest_framework.generics import get_object_or_404
from simpleeval import SimpleEval

from common.exceptions import UnknownCommandException
from dua_empat.models import Question


class AnswerSelector:
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }
    _evaluator = SimpleEval(operators=_operators)

    @classmethod
    def get_and_validate_answer(cls, source_id: str, text: str) -> int:
        question = get_object_or_404(Question, source_id=source_id)

        cls._validate_formula(text)
        cls._validate_numbers(question.numbers, text)

        return cls._evaluator.eval(text)

    @staticmethod
    def _validate_formula(text: str):
        non_formula_text = re.search(r'[^ ()*+\-/0-9]', text)
        if non_formula_text is not None:
            raise UnknownCommandException

    @staticmethod
    def _validate_numbers(numbers: tuple, text: str):
        text_numbers = re.split(r'[^0-9]', text)
        text_numbers = filter(None, text_numbers)
        text_numbers = (int(text) for text in text_numbers)
        numbers = sorted(numbers)
        text_numbers = sorted(text_numbers)
        if numbers != text_numbers:
            raise UnknownCommandException
