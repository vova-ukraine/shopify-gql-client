from base_types import ScalarType
from exceptions import ValidationError

class String(ScalarType, str):

    @classmethod
    def validate(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"Invalid String value: {value}")
        return value