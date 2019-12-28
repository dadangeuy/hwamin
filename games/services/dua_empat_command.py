from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from accounts.services import RetrieveProfileService
from chats.services import CreateReplyService
from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable
from games.services.dua_empat_calculator import DuaEmpatCalculatorService
from games.services.dua_empat_generator import DuaEmpatGeneratorService
from games.services.dua_empat_solver import DuaEmpatSolverService


class DuaEmpatCommandService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, profile: Profile) -> None:
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

            messages.append('game selesai')

        elif text == 'ulang':
            messages.append(session['question'].__str__())

        elif text == 'nyerah':
            answer = DuaEmpatSolverService.run(session['question']) or 'tidak ada'
            cls._update_scores(session, profile, -1)
            cls._create_new_question(session)

            messages.append(f'jawabannya {answer}')
            messages.append(cls._get_scoreboard(session))
            messages.append(session['question'].__str__())

        elif text == 'tidak ada':
            answer = DuaEmpatSolverService.run(session['question'])

            if answer is None:
                cls._update_scores(session, profile, 1)
                cls._create_new_question(session)

                messages.append('tidak ada!!')
                messages.append(cls._get_scoreboard(session))
                messages.append(session['question'].__str__())

            else:
                cls._update_scores(session, profile, -1)

                messages.append('ada jawabannya loh')

        else:
            try:
                numbers = session['question']
                result = DuaEmpatCalculatorService.run(numbers, text)

                if result == 24:
                    cls._update_scores(session, profile, 1)
                    cls._create_new_question(session)

                    messages.append('dua empat!!')
                    messages.append(cls._get_scoreboard(session))
                    messages.append(session['question'].__str__())

                else:
                    cls._update_scores(session, profile, -1)

                    messages.append(f'{text} hasilnya {result:g}')

            except UnknownCommandException:
                ...

        CreateReplyService.run(token, messages)

    @staticmethod
    def _update_scores(session: SessionBase, profile: Profile, score: int) -> None:
        scoreboard = session['scoreboard']
        current_score = scoreboard.get(profile.id, 0)
        scoreboard[profile.id] = current_score + score
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
            f'{RetrieveProfileService.run(profile_id).name}: {score}'
            for profile_id, score in scoreboard.items()
        ]
        score_text = '\n'.join(score_texts)

        return header_text + score_text
