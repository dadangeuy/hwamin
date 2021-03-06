from typing import List

from common.exceptions import UnknownCommandException
from dua_empat.selectors import AnswerSelector, QuestionSelector, SolutionSelector
from dua_empat.services import UpdateOrCreateQuestionService
from session.client import SessionClient


class DuaEmpatClient:

    @staticmethod
    def start(source_id: str) -> List[str]:
        question = UpdateOrCreateQuestionService.run(source_id)
        return ['game dimulai', question.display_numbers]

    @staticmethod
    def end(source_id: str) -> List[str]:
        score_board = SessionClient.get_score_board(source_id)
        return [score_board, 'game selesai']

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
        question = QuestionSelector.get_question(source_id)
        return [question.display_numbers]

    @classmethod
    def _give_up(cls, source_id: str) -> List[str]:
        answer = SolutionSelector.get_solution(source_id) or 'tidak ada'
        score_board = SessionClient.get_score_board(source_id)
        question = UpdateOrCreateQuestionService.run(source_id)
        return [f'jawabannya {answer}', score_board, question.display_numbers]

    @classmethod
    def _try_answer(cls, source_id: str, profile_id: str, text: str) -> List[str]:
        if text == 'tidak ada':
            answer = SolutionSelector.get_solution(source_id)
            is_correct = answer is None

            if is_correct:
                SessionClient.update_score(source_id, profile_id, 1)
                score_board = SessionClient.get_score_board(source_id)
                question = UpdateOrCreateQuestionService.run(source_id)
                return [score_board, question.display_numbers]

            else:
                SessionClient.update_score(source_id, profile_id, -1)
                return ['ada jawabannya loh']

        else:
            try:
                result = AnswerSelector.get_and_validate_answer(source_id, text)
                is_correct = result == 24

                if is_correct:
                    SessionClient.update_score(source_id, profile_id, 1)
                    score_board = SessionClient.get_score_board(source_id)
                    question = UpdateOrCreateQuestionService.run(source_id)
                    return [score_board, question.display_numbers]

                else:
                    SessionClient.update_score(source_id, profile_id, -1)
                    return [f'{text} = {result:g}']

            except UnknownCommandException:
                return []
