import pytest

from dua_empat.models import Question
from dua_empat.selectors import SolutionSelector
from dua_empat.tests.factories.question import QuestionFactory


@pytest.mark.django_db
class TestSolutionSelector:
    selector = SolutionSelector

    def test_has_solution(self):
        question = self._create_question(1, 1, 12, 12)
        solution = self.selector.get_solution(question.source_id)
        assert solution is not None

    def test_has_no_solution(self):
        question = self._create_question(13, 13, 13, 13)
        solution = self.selector.get_solution(question.source_id)
        assert solution is None

    def test_has_solution_2(self):
        question = self._create_question(1, 7, 9, 10)
        solution = self.selector.get_solution(question.source_id)
        assert solution is not None

    def _create_question(self, *numbers: int) -> Question:
        question = QuestionFactory(
            first_number=numbers[0],
            second_number=numbers[1],
            third_number=numbers[2],
            fourth_number=numbers[3],
        )
        return question
