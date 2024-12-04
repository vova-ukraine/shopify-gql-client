from .scalar import Scalar
from .exceptions import ValidationError

class String(Scalar):

    @staticmethod
    def validate(value: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"Invalid String value: {value}")
        return value