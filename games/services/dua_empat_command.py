from typing import List

from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from chats.services import CreateTextReplyService
from commons.exceptions import UnknownCommandException
from commons.patterns import Runnable
from dua_empat.services import QuestionService, AnswerService
from games.models import Play
from games.services.play import PlayService
from games.services.score import ScoreService


class DuaEmpatCommandService(Runnable):
    @classmethod
    def run(cls, token: str, text: str, source_id: str, profile: Profile) -> None:
        if text == 'main 24':
            messages = cls._start(source_id)
        elif text == 'udahan':
            messages = cls._end(source_id)
        elif text == 'ulang':
            messages = cls._retry(source_id)
        elif text == 'nyerah':
            messages = cls._give_up(source_id)
        else:
            messages = cls._try_answer(source_id, profile.id, text)

        CreateTextReplyService.run(token, messages)
        
    @classmethod
    def _start(cls, source_id: str) -> List[str]:
        PlayService.start(source_id, Play.Game.DUA_EMPAT)
        question = QuestionService.get_new_question(source_id)
        return ['game dimulai', question.display_numbers]

    @classmethod
    def _end(cls, source_id: str) -> List[str]:
        score_info = ScoreService.get_info(source_id)
        ScoreService.clear(source_id)
        QuestionService.clear(source_id)
        PlayService.end(source_id)
        return [score_info, 'game selesai']

    @classmethod
    def _retry(cls, source_id: str) -> List[str]:
        question = QuestionService.get_question(source_id)
        return [question.display_numbers]

    @classmethod
    def _give_up(cls, source_id: str) -> List[str]:
        answer = AnswerService.get_answer(source_id) or 'tidak ada'
        score_info = ScoreService.get_info(source_id)
        question = QuestionService.get_new_question(source_id)
        return [f'jawabannya {answer}', score_info, question.display_numbers]

    @classmethod
    def _try_answer(cls, source_id: str, profile_id: str, text: str) -> List[str]:
        if text == 'tidak ada':
            answer = AnswerService.get_answer(source_id)
            is_correct = answer is None

            if is_correct:
                ScoreService.add_point(source_id, profile_id, 1)
                score_info = ScoreService.get_info(source_id)
                question = QuestionService.get_new_question(source_id)
                return [score_info, question.display_numbers]
                
            else:
                ScoreService.add_point(source_id, profile_id, -1)
                return ['ada jawabannya loh']
        
        else:
            try:
                AnswerService.validate_answer(source_id, text)
                result = AnswerService.get_result(text)
                is_correct = result == 24
                
                if is_correct:
                    ScoreService.add_point(source_id, profile_id, 1)
                    score_info = ScoreService.get_info(source_id)
                    question = QuestionService.get_new_question(source_id)
                    return [score_info, question.display_numbers]
                
                else:
                    ScoreService.add_point(source_id, profile_id, -1)
                    return [f'{text} = {result:g}']
                
            except UnknownCommandException:
                return []
