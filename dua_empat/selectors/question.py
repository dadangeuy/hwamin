from dua_empat.models.question import Question


class QuestionSelector:

    @classmethod
    def get_question(cls, source_id: str) -> Question:
        question = Question.objects.filter(source_id=source_id).first()
        return question
