from dataclasses import dataclass
from typing import List, Union

from dataclasses_json import dataclass_json, LetterCase

from ..actions import Postback



@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Column:
    text: str
    actions: List[Union[Postback]]
    thumbnail_image_url: str = None
    image_background_color: str = '#FFFFFF'
    title: str = None
    default_action: Union[Postback] = None
