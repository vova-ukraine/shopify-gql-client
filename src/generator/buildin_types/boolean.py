from base_types import ScalarType
from exceptions import ValidationError

class Boolean(ScalarType, bool):
    @classmethod
    def validate(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValidationError(f"Invalid Boolean value: {value}")
        return value