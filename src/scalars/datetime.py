import re
from .scalar import Scalar
from .exceptions import ValidationError

#Represents an ISO 8601-encoded date and time string. For example, 3:50 pm on September 7, 2019 in the time zone of UTC (Coordinated Universal Time) is represented as "2019-09-07T15:50:00Z".
class DateTime(Scalar):
    def validate(cls, value: str) -> str:
        date_time_regex = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        if not date_time_regex.match(value):
            raise ValidationError(f"Invalid DateTime value: {value}")
        return value
