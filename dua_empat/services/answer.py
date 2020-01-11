import ast
import operator
import re
from itertools import permutations
from typing import Optional

from rest_framework.generics import get_object_or_404
from simpleeval import SimpleEval

from commons.exceptions import UnknownCommandException
from dua_empat.models import Question


class AnswerService:
    _operator_by_text = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }
    _evaluator = SimpleEval(operators=_operators)

    @classmethod
    def get_answer(cls, source_id: str) -> Optional[str]:
        question = get_object_or_404(Question, source_id=source_id)
        variables = question.numbers

        for v0, v1, v2, v3 in permutations(sorted(variables)):
            for n0, o0 in cls._operator_by_text.items():
                for n1, o1 in cls._operator_by_text.items():
                    for n2, o2 in cls._operator_by_text.items():

                        try:
                            result = o2(o1(o0(v0, v1), v2), v3)
                            if result == 24:
                                return f'(({v0} {n0} {v1}) {n1} {v2}) {n2} {v3}'
                        except ZeroDivisionError:
                            ...

                        try:
                            result = o2(o0(v0, v1), o1(v2, v3))
                            if result == 24:
                                return f'({v0} {n0} {v1}) {n2} ({v2} {n1} {v3})'
                        except ZeroDivisionError:
                            ...

    @classmethod
    def validate_answer(cls, source_id: str, text: str) -> None:
        if text != 'tidak ada':
            question = get_object_or_404(Question, source_id=source_id)
            cls._validate_formula(text)
            cls._validate_numbers(question.numbers, text)

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


    @classmethod
    def get_result(cls, text: str) -> int:
        return cls._evaluator.eval(text)
