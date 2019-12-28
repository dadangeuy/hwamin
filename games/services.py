import ast
import operator
import re
from itertools import permutations
from typing import List

from django.contrib.sessions.backends.base import SessionBase
from factory.fuzzy import FuzzyInteger
from simpleeval import SimpleEval

from accounts.services import RetrieveProfileService
from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable
from externals.services import CreateReplyLineService


class DuaEmpatGeneratorService(Runnable):
    FUZZY_INTEGER = FuzzyInteger(low=1, high=13)

    @classmethod
    def run(cls) -> List[int]:
        return [
            cls._get_random_int(),
            cls._get_random_int(),
            cls._get_random_int(),
            cls._get_random_int()
        ]

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
            raise UnknownCommandException

    @staticmethod
    def _validate_numbers(numbers: List[int], text: str):
        text_numbers = re.split(r'[^0-9]', text)
        text_numbers = filter(None, text_numbers)
        text_numbers = [int(text) for text in text_numbers]
        numbers = sorted(numbers)
        text_numbers = sorted(text_numbers)
        if numbers != text_numbers:
            raise UnknownCommandException


class DuaEmpatReplyService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, user_id: str) -> None:
        messages = []

        if text == 'udahan':
            session.clear()
            messages.append('game selesai')

        elif text == 'ulang':
            messages.append(session['question'].__str__())

        elif text == 'nyerah':
            answer = DuaEmpatSolverService.run(session['question']) or 'tidak ada'
            messages.append(f'jawabannya {answer}')

            cls._update_scores(session, user_id, -1)
            messages.append(cls._get_scoreboard(session))

            cls._create_new_question(session)
            messages.append(session['question'].__str__())

        elif text == 'tidak ada':
            answer = DuaEmpatSolverService.run(session['question'])

            if answer is None:
                messages.append('tidak ada!!')
                cls._update_scores(session, user_id, 1)
                messages.append(cls._get_scoreboard(session))
                cls._create_new_question(session)
                messages.append(session['question'].__str__())

            else:
                messages.append('ada jawabannya loh')
                cls._update_scores(session, user_id, -1)

        else:
            try:
                numbers = session['question']
                result = DuaEmpatCalculatorService.run(numbers, text)

                if result == 24:
                    messages.append('dua empat!!')
                    cls._update_scores(session, user_id, 1)
                    messages.append(cls._get_scoreboard(session))
                    cls._create_new_question(session)
                    messages.append(session['question'].__str__())

                else:
                    messages.append(f'{text} hasilnya {result:g}')
                    cls._update_scores(session, user_id, -1)

            except UnknownCommandException:
                ...  # ignored

        CreateReplyLineService.run(token, messages)

    @staticmethod
    def _update_scores(session: SessionBase, user_id: str, score: int) -> None:
        scoreboard = session['scoreboard']
        current_score = scoreboard.get(user_id, 0)
        scoreboard[user_id] = current_score + score
        session['score'] = scoreboard

    @staticmethod
    def _create_new_question(session: SessionBase) -> None:
        question = DuaEmpatGeneratorService.run()
        session['question'] = question

    @staticmethod
    def _get_scoreboard(session: SessionBase) -> str:
        scoreboard = session['scoreboard']
        header_text = '[SCOREBOARD]\n'
        score_texts = [
            f'{RetrieveProfileService.run(user_id).name}: {score}'
            for user_id, score in scoreboard.items()
        ]
        score_text = '\n'.join(score_texts)

        return header_text + score_text


class StartGameService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str) -> None:
        messages = []

        if text == 'main 24':
            session['question'] = DuaEmpatGeneratorService.run()
            session['game'] = 'DUA_EMPAT'
            session['scoreboard'] = {}
            messages.append('game dimulai')
            messages.append(session['question'].__str__())

        CreateReplyLineService.run(token, messages)


class TextService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, user_id: str) -> None:
        game = session.get('game', None)
        if game is None:
            StartGameService.run(session, token, text)
        elif game == 'DUA_EMPAT':
            DuaEmpatReplyService.run(session, token, text, user_id)
