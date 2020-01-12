from session.services import DuaEmpatSolverService


class TestDuaEmpatSolverService:

    def test_has_answer(self):
        question = [1, 1, 12, 12]
        answer = DuaEmpatSolverService.run(question)
        assert answer is not None

    def test_has_no_answer(self):
        question = [13, 13, 13, 13]
        answer = DuaEmpatSolverService.run(question)
        assert answer is None

    def test_has_answer_2(self):
        question = [1, 7, 9, 10]
        answer = DuaEmpatSolverService.run(question)
        assert answer is not None