from base_types import ScalarType
from exceptions import ValidationError

class Int(ScalarType, int):
    
    @classmethod
    def validate(cls, value: int) -> int:
        if not isinstance(value, int):
            raise ValidationError(f"Invalid Int value: {value}")
        return value