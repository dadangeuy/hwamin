import ast
import operator

from simpleeval import SimpleEval

from commons.patterns import Runnable


class DuaEmpatCalculatorService(Runnable):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }
    EVAL = SimpleEval(operators=OPERATORS)

    @classmethod
    def run(cls, text: str) -> bool:
        return cls.EVAL.eval(text)
