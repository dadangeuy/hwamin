from abc import ABC

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
class Message(ABC):
    ...
