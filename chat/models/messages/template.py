from dataclasses import dataclass
from typing import Union

from dataclasses_json import dataclass_json, LetterCase

from .base import Message
from ..templates import Carousel


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Template(Message):
    alt_text: str
    template: Union[Carousel]
    type: str = 'template'
