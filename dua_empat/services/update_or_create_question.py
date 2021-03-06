from factory.fuzzy import FuzzyInteger

from common.patterns import Runnable
from dua_empat.models import Question


class UpdateOrCreateQuestionService(Runnable):
    number_factory = FuzzyInteger(low=0, high=13)

    @classmethod
    def run(cls, source_id: str) -> Question:
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