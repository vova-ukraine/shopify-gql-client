import datetime
import re
from .scalar import Scalar
from .exceptions import ValidationError

#Represents an ISO 8601-encoded date string. For example, September 7, 2019 is represented as "2019-07-16".
class Date(Scalar):
    def validate(cls, value: datetime.date) -> datetime.date:
        date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_regex.match(value):
            raise ValidationError(f"Invalid Date value: {value}")
        return value
