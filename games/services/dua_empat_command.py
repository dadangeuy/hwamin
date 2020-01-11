from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from chats.services import CreateTextReplyService
from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable
from games.services.dua_empat_calculator import DuaEmpatCalculatorService
from games.services.dua_empat_generator import DuaEmpatGeneratorService
from games.services.dua_empat_solver import DuaEmpatSolverService
from games.services.score import ScoreService


class DuaEmpatCommandService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, source_id: str, profile: Profile) -> None:
        messages = []

        if text == 'main 24':
            session.clear()
            session['question'] = DuaEmpatGeneratorService.run()
            session['game'] = 'DUA_EMPAT'
            session['scoreboard'] = {}

            messages.append('game dimulai')
            messages.append(session['question'].__str__())

        if text == 'udahan':
            session.clear()
            ScoreService.clear(source_id)

            messages.append('game selesai')

        elif text == 'nyerah':
            answer = DuaEmpatSolverService.run(session['question']) or 'tidak ada'
            cls._update_scores(source_id, profile, -1)
            cls._create_new_question(session)

            messages.append(f'jawabannya {answer}')
            messages.append(cls._get_scoreboard(source_id))
            messages.append(session['question'].__str__())

        elif text == 'tidak ada':
            answer = DuaEmpatSolverService.run(session['question'])

            if answer is None:
                cls._update_scores(source_id, profile, 1)
                cls._create_new_question(session)

                messages.append('tidak ada!!')
                messages.append(cls._get_scoreboard(source_id))
                messages.append(session['question'].__str__())

            else:
                cls._update_scores(source_id, profile, -1)

                messages.append('ada jawabannya loh')

        else:
            try:
                numbers = session['question']
                result = DuaEmpatCalculatorService.run(numbers, text)

                if result == 24:
                    cls._update_scores(source_id, profile, 1)
                    cls._create_new_question(session)

                    messages.append('dua empat!!')
                    messages.append(cls._get_scoreboard(source_id))
                    messages.append(session['question'].__str__())

                else:
                    cls._update_scores(source_id, profile, -1)

                    messages.append(f'{text} hasilnya {result:g}')

            except UnknownCommandException:
                ...

        CreateTextReplyService.run(token, messages)

    @staticmethod
    def _update_scores(source_id: str, profile: Profile, score: int) -> None:
        ScoreService.add_point(source_id, profile.id, score)

    @staticmethod
    def _create_new_question(session: SessionBase) -> None:
        question = DuaEmpatGeneratorService.run()
        session['question'] = question

    @staticmethod
    def _get_scoreboard(source_id: str) -> str:
        return ScoreService.get_info(source_id)
