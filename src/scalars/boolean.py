from .scalar import Scalar
from .exceptions import ValidationError


class Boolean(Scalar):
    def validate(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValidationError(f"Invalid Boolean value: {value}")
        return value