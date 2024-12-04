from .scalar import Scalar
from .exceptions import ValidationError

class Int(Scalar):
    @staticmethod
    def build(value: int) -> int:
        if not isinstance(value, int):
            raise ValidationError(f"Invalid Int value: {value}")
        if value < -(2**31) or value > (2**31 - 1):
            raise ValidationError(f"Int value out of range: {value}")
        return value