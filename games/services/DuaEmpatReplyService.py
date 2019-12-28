from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from accounts.services import RetrieveProfileService
from chats.services import CreateReplyService
from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable
from games.services import DuaEmpatSolverService, DuaEmpatCalculatorService, DuaEmpatGeneratorService


class DuaEmpatReplyService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, profile: Profile) -> None:
        messages = []

        if text == 'udahan':
            session.clear()
            messages.append('game selesai')

        elif text == 'ulang':
            messages.append(session['question'].__str__())

        elif text == 'nyerah':
            answer = DuaEmpatSolverService.run(session['question']) or 'tidak ada'
            messages.append(f'jawabannya {answer}')

            cls._update_scores(session, profile, -1)
            messages.append(cls._get_scoreboard(session))

            cls._create_new_question(session)
            messages.append(session['question'].__str__())

        elif text == 'tidak ada':
            answer = DuaEmpatSolverService.run(session['question'])

            if answer is None:
                messages.append('tidak ada!!')
                cls._update_scores(session, profile, 1)
                messages.append(cls._get_scoreboard(session))
                cls._create_new_question(session)
                messages.append(session['question'].__str__())

            else:
                messages.append('ada jawabannya loh')
                cls._update_scores(session, profile, -1)

        else:
            try:
                numbers = session['question']
                result = DuaEmpatCalculatorService.run(numbers, text)

                if result == 24:
                    messages.append('dua empat!!')
                    cls._update_scores(session, profile, 1)
                    messages.append(cls._get_scoreboard(session))
                    cls._create_new_question(session)
                    messages.append(session['question'].__str__())

                else:
                    messages.append(f'{text} hasilnya {result:g}')
                    cls._update_scores(session, profile, -1)

            except UnknownCommandException:
                ...  # ignored

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
