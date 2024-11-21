from dataclasses import dataclass, field

from domain.exception.value_ex.ex_base_value import (FrozenSmallTextTypeError,
                                                        FrozenSmallTextLengthError)

@dataclass(frozen=True)
class FrozenSmallText:
    text: str

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise FrozenSmallTextTypeError(f"Текст должен быть типа str")
        if len(self.text) > 256 or len(self.text) < 2:
            raise FrozenSmallTextLengthError(
                f"Длина текста должна быть в диапазоне [2,256]\n"\
                f"Ваш текст длинной {len(self.text)}"
                )
