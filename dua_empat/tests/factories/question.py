from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyInteger

from dua_empat.models import Question


class QuestionFactory(DjangoModelFactory):
    first_number = FuzzyInteger(low=0, high=13)
    second_number = FuzzyInteger(low=0, high=13)
    third_number = FuzzyInteger(low=0, high=13)
    fourth_number = FuzzyInteger(low=0, high=13)
    source_id = FuzzyText(length=33)

    class Meta:
        model = Question
