from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from .base import Message


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Text(Message):
    text: str
    type: str = 'text'
