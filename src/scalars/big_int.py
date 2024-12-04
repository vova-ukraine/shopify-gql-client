from .scalar import Scalar


# Represents non-fractional signed whole numeric values. Since the value may exceed the size of a 32-bit integer, it's encoded as a string.
class BigInt(Scalar):
    @classmethod
    def validate(cls, value: int) -> int:
        if not isinstance(value, int):
            raise ValidationError(f"Invalid BigInt value: {value}")
        return value
