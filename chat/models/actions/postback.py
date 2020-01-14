from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Postback:
    data: str
    label: str = None
    display_text: str = None
    text: str = None
    type: str = 'postback'
