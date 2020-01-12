from common.patterns import Runnable
from dua_empat.models.question import Question


class GetQuestionService(Runnable):

    @classmethod
    def run(cls, source_id: str) -> Question:
        question = Question.objects.filter(source_id=source_id).first()
        return question
