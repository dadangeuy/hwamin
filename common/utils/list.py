from collections import defaultdict
from typing import TypeVar, List, Callable, Dict


class ListUtil:
    K = TypeVar(name='K')
    V = TypeVar(name='V')

    @staticmethod
    def distinct_group_by(items: List[V], key_fn: Callable[[V], K]) -> Dict[K, V]:
        return {key_fn(item): item for item in items}

    @staticmethod
    def group_by(items: List[V], key_fn: Callable[[V], K]) -> Dict[K, List[V]]:
        grouping = defaultdict(list)
        for item in items:
            grouping[key_fn(item)].append(item)
        return grouping
