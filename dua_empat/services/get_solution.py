import operator
from itertools import permutations
from typing import Optional

from rest_framework.generics import get_object_or_404

from common.patterns import Runnable
from dua_empat.models import Question


class GetSolutionService(Runnable):
    _operator_by_text = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    @classmethod
    def run(cls, source_id: str) -> Optional[str]:
        question = get_object_or_404(Question, source_id=source_id)
        variables = question.numbers

        for v0, v1, v2, v3 in permutations(sorted(variables)):
            for n0, o0 in cls._operator_by_text.items():
                for n1, o1 in cls._operator_by_text.items():
                    for n2, o2 in cls._operator_by_text.items():

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
