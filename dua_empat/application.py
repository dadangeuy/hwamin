from typing import List

from common.exceptions import UnknownCommandException
from dua_empat.services import QuestionService, AnswerService
from session.application import SessionApplication


class DuaEmpatApplication:
    @classmethod
    def start(cls, source_id: str) -> List[str]:
        question = QuestionService.get_new_question(source_id)
        return ['game dimulai', question.display_numbers]

    @classmethod
    def end(cls, source_id: str) -> List[str]:
        score_info = SessionApplication.get_score_info(source_id)
        return [score_info, 'game selesai']

    @classmethod
    def reply(cls, source_id: str, profile_id: str, text: str) -> List[str]:
        text = text.lower()
        return (
            cls._retry(source_id) if text == 'ulang' else
            cls._give_up(source_id) if text == 'nyerah' else
            cls._try_answer(source_id, profile_id, text)
        )

    @classmethod
    def _retry(cls, source_id: str) -> List[str]:
        question = QuestionService.get_question(source_id)
        return [question.display_numbers]

    @classmethod
    def _give_up(cls, source_id: str) -> List[str]:
        answer = AnswerService.get_answer(source_id) or 'tidak ada'
        score_info = SessionApplication.get_score_info(source_id)
        question = QuestionService.get_new_question(source_id)
        return [f'jawabannya {answer}', score_info, question.display_numbers]

    @classmethod
    def _try_answer(cls, source_id: str, profile_id: str, text: str) -> List[str]:
        if text == 'tidak ada':
            answer = AnswerService.get_answer(source_id)
            is_correct = answer is None

            if is_correct:
                SessionApplication.add_point(source_id, profile_id, 1)
                score_info = SessionApplication.get_score_info(source_id)
                question = QuestionService.get_new_question(source_id)
                return [score_info, question.display_numbers]

            else:
                SessionApplication.add_point(source_id, profile_id, -1)
                return ['ada jawabannya loh']

        else:
            try:
                AnswerService.validate_answer(source_id, text)
                result = AnswerService.get_result(text)
                is_correct = result == 24

                if is_correct:
                    SessionApplication.add_point(source_id, profile_id, 1)
                    score_info = SessionApplication.get_score_info(source_id)
                    question = QuestionService.get_new_question(source_id)
                    return [score_info, question.display_numbers]

                else:
                    SessionApplication.add_point(source_id, profile_id, -1)
                    return [f'{text} = {result:g}']

            except UnknownCommandException:
                return []
