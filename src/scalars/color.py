import re
from .scalar import Scalar
from .exceptions import ValidationError

# A string containing a hexadecimal representation of a color.
# For example, "#6A8D48".
class Color(Scalar):
    def validate(cls, value: str) -> str:
        color_regex = re.compile(r"^#[0-9A-F]{6}$")
        if not color_regex.match(value):
            raise ValidationError(f"Invalid Color value: {value}")
        return value
