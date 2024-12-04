from base_types import ScalarType
from exceptions import ValidationError


class Float(ScalarType, float):
    
    @classmethod
    def validate(cls, value: float) -> float:
        if not isinstance(value, float):
            raise ValidationError(f"Invalid Float value: {value}")
        return value