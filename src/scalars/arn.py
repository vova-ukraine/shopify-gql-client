import re
from typing import Any
from .scalar import Scalar
from .exceptions import ValidationError


class ARN(Scalar):
    @classmethod
    def validate(cls, value: Any) -> Any:
        aws_arn_regex = re.compile(
            r"^arn:aws:[a-zA-Z0-9-]+:[a-zA-Z0-9-]*:[0-9]*:[^:]*(:[^:]*)?$"
        )
        if not aws_arn_regex.match(value):
            raise ValidationError(f"Invalid ARN value: {value}")
        return value
