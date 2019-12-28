import operator
from itertools import permutations
from typing import List

from commons.patterns import Runnable


class DuaEmpatSolverService(Runnable):
    OPERATOR_BY_NAME = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    @classmethod
    def run(cls, variables: List[int]) -> str:
        for v0, v1, v2, v3 in permutations(sorted(variables)):
            for n0, o0 in cls.OPERATOR_BY_NAME.items():
                for n1, o1 in cls.OPERATOR_BY_NAME.items():
                    for n2, o2 in cls.OPERATOR_BY_NAME.items():

                        try:
                            result = o2(o1(o0(v0, v1), v2), v3)
                            if result == 24:
                                return f'(({v0} {n0} {v1}) {n1} {v2}) {n2} {v3}'
                        except ZeroDivisionError:
                            ...

                        try:
                            result = o2(o0(v0, v1), o1(v2, v3))
                            if result == 24:
                                return f'({v0} {n0} {v1}) {n2} ({v2} {n1} {v3})'
                        except ZeroDivisionError:
                            ...
