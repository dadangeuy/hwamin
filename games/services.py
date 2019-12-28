import ast
import operator
import re
from itertools import permutations
from typing import Tuple, List, Optional

from django.contrib.sessions.backends.base import SessionBase
from factory.fuzzy import FuzzyInteger
from simpleeval import SimpleEval

from commons.patterns import Runnable
from externals.services import CreateReplyLineService


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


class DuaEmpatSolverService(Runnable):
    OPERATORS = [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv
    ]
    TEXT_BY_OPERATOR = {
        operator.add: '+',
        operator.sub: '-',
        operator.mul: '*',
        operator.truediv: '/'
    }

    @classmethod
    def run(cls, numbers: List[int]) -> str:
        numbers = sorted(numbers)
        for numbers in permutations(numbers):
            for operator_a_b in cls.OPERATORS:
                for operator_ab_c in cls.OPERATORS:
                    for operator_abc_d in cls.OPERATORS:
                        a = numbers[0]
                        b = numbers[1]
                        c = numbers[2]
                        d = numbers[3]
                        result = operator_abc_d(operator_ab_c(operator_a_b(a, b), c), d)
                        if result == 24:
                            a_b_op = cls.TEXT_BY_OPERATOR[operator_a_b]
                            ab_c_op = cls.TEXT_BY_OPERATOR[operator_ab_c]
                            abc_d_op = cls.TEXT_BY_OPERATOR[operator_abc_d]
                            return f'(({a}{a_b_op}{b}){ab_c_op}{c}){abc_d_op}{d}'


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


class DuaEmpatReplyService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str) -> None:
        if text == 'udahan':
            session.clear()
            messages = ['game selesai']
        elif text == 'ulang':
            numbers = session['numbers']
            messages = [numbers.__str__()]
        elif text == 'nyerah':
            numbers = session['numbers']
            answer = DuaEmpatSolverService.run(numbers) or 'tidak ada'
            numbers = DuaEmpatGeneratorService.run()
            session['numbers'] = numbers
            messages = [f'jawabannya {answer}', numbers.__str__()]
        elif text == 'tidak ada':
            numbers = session['numbers']
            answer = DuaEmpatSolverService.run(numbers)
            has_answer = answer is not None
            if has_answer:
                messages = ['ada jawabannya loh']
            else:
                numbers = DuaEmpatGeneratorService.run()
                session['numbers'] = numbers
                messages = ['tidak ada!!', numbers.__str__()]
        else:
            numbers = session['numbers']
            result = DuaEmpatCalculatorService.run(numbers, text)
            is_24 = result == 24
            if is_24:
                numbers = DuaEmpatGeneratorService.run()
                session['numbers'] = numbers
                messages = ['dua empat!!', numbers.__str__()]
            else:
                messages = [f'{text} hasilnya {result:g}']

        CreateReplyLineService.run(token, messages)


class StartGameService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str) -> None:
        messages = None

        if text == 'main 24':
            numbers = DuaEmpatGeneratorService.run()
            session['game'] = 'DUA_EMPAT'
            session['numbers'] = numbers
            messages = ['game dimulai', numbers.__str__()]

        CreateReplyLineService.run(token, messages)


class TextService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str) -> None:
        game = session.get('game', None)
        if game is None:
            StartGameService.run(session, token, text)
        elif game == 'DUA_EMPAT':
            DuaEmpatReplyService.run(session, token, text)
