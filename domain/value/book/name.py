import re
from dataclasses import dataclass, field
from typing import Optional

from domain.value.base_value import FrozenSmallText
from domain.exception.value_ex.exception_author import NameError


@dataclass(frozen=True)
class Name:
    first_name: FrozenSmallText
    last_name: FrozenSmallText
    middle_name: Optional[FrozenSmallText] = field(default=None)

    def __post_init__(self):
        s = ""
        if self.middle_name:
            s = self.middle_name.text
        if not re.fullmatch(
            r"[а-яА-яa-zA-z]+", 
            self.first_name.text+self.last_name.text+s):
            raise NameError(f"Имя должно состоять только из кириллицы или латиницы\
                \nВы ввели: {str(self)}")
    
    def __str__(self):
        parts = [self.first_name.text]
        if self.middle_name:
            parts.append(self.middle_name.text)
        parts.append(self.last_name.text)
        return " ".join(str(part) for part in parts)