from domain.exception.base_exception import BaseException


class FrozenSmallTextTypeError(BaseException):
    """
    Исключениие для FrozenSmallText при неверно переданном типе
    """
    ...
class FrozenSmallTextLengthError(BaseException):
    """
    Исключениие для FrozenSmallText при неверной длине текста
    """
    ...