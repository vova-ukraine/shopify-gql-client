from base_types import ScalarType
from exceptions import ValidationError

class ID(ScalarType, str):
    @classmethod
    def validate(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"Invalid ID value: {value}")
        return value