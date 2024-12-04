from .base import Base


class Scalar(Base):
    # Return validated value
    def __new__(cls, value: str) -> str:
        return cls.validate(value)

    @classmethod
    def validate(cls, value):
        return value
