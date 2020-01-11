from factory.fuzzy import FuzzyInteger

from dua_empat.models.question import Question


class QuestionService:
    number_factory = FuzzyInteger(low=0, high=13)

    @classmethod
    def get_question(cls, source_id: str) -> Question:
        question = Question.objects.filter(source_id=source_id).first()
        return question

    @classmethod
    def get_new_question(cls, source_id: str) -> Question:
        question, _ = Question.objects.update_or_create(
            source_id=source_id,
            defaults={
                'first_number': cls.number_factory.fuzz(),
                'second_number': cls.number_factory.fuzz(),
                'third_number': cls.number_factory.fuzz(),
                'fourth_number': cls.number_factory.fuzz()
            }
        )
        return question

    @classmethod
    def clear(cls, source_id: str) -> None:
        Question.objects.filter(source_id=source_id)
