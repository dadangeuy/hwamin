from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from chats.services import CreateTextReplyService
from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable
from duaempat.services import QuestionService
from games.services.dua_empat_calculator import DuaEmpatCalculatorService
from games.services.dua_empat_solver import DuaEmpatSolverService
from games.services.score import ScoreService


class DuaEmpatCommandService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, source_id: str, profile: Profile) -> None:
        messages = []

        if text == 'main 24':
            session.clear()
            session['game'] = 'DUA_EMPAT'

            question = QuestionService.get_new_question(source_id)

            messages.append('game dimulai')
            messages.append(question.display_numbers)

        if text == 'udahan':
            session.clear()
            ScoreService.clear(source_id)
            QuestionService.clear(source_id)

            messages.append('game selesai')

        elif text == 'nyerah':
            question = QuestionService.get_question(source_id)
            answer = DuaEmpatSolverService.run(question.numbers) or 'tidak ada'

            ScoreService.add_point(source_id, profile.id, -1)
            new_question = QuestionService.get_new_question(source_id)

            score_info = ScoreService.get_info(source_id)

            messages.append(f'jawabannya {answer}')
            messages.append(score_info)
            messages.append(new_question)

        elif text == 'tidak ada':
            question = QuestionService.get_question(source_id)
            answer = DuaEmpatSolverService.run(question.numbers)

            if answer is None:
                ScoreService.add_point(source_id, profile.id, 1)
                question = QuestionService.get_new_question(source_id)

                score_info = ScoreService.get_info(source_id)

                messages.append(score_info)
                messages.append(question.display_numbers)

            else:
                ScoreService.add_point(source_id, profile.id, -1)

                messages.append('ada jawabannya loh')

        else:
            try:
                question = QuestionService.get_question(source_id)
                result = DuaEmpatCalculatorService.run(question.numbers, text)

                if result == 24:
                    ScoreService.add_point(source_id, profile.id, 1)
                    new_question = QuestionService.get_new_question(source_id)
                    score_info = ScoreService.get_info(source_id)

                    messages.append(score_info)
                    messages.append(new_question.display_numbers)

                else:
                    ScoreService.add_point(source_id, profile.id, -1)

                    messages.append(f'{text} hasilnya {result:g}')

            except UnknownCommandException:
                ...

        CreateTextReplyService.run(token, messages)
