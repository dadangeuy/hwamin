from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json, LetterCase

from ..others import Column


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Carousel:
    columns: List[Column]  # max 10
    image_aspect_ratio: str = 'rectangle'  # rectangle, square
    image_size: str = 'cover'  # cover, contain
    type: str = 'carousel'
