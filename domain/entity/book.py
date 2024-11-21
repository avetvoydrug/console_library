from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from domain.entity.base_entity import BaseEntity
from domain.exception.entity_ex.book import BookError
from domain.exception.value_ex.exception_author import NameError
from domain.value.base_value import FrozenSmallText
from domain.value.book.statusenum import StatusEnum
from domain.value.book.name import Name


@dataclass
class Book(BaseEntity):
    title: FrozenSmallText
    year: int
    author: Name
    status: str = field(default=StatusEnum.AVAILABLE)

    def __post_init__(self):
        if not isinstance(self.title, FrozenSmallText):
            raise BookError("title должен быть типа FrozenSmallText")
        if not isinstance(self.author, Name):
            raise NameError("author должен быть типа Name")
        if not isinstance(self.status, str) and \
            self.status not in StatusEnum:
            raise BookError("статус должен быть типа StatusEnum"\
                "\nили передан строкой как: 'в наличии' или 'выдана'")
        if not isinstance(self.year, int):
            raise BookError("Год должен быть типа int")
        if self.year < 0 or self.year > datetime.now().year:
            raise BookError("Год не может быть в будущем или отрицательным")
