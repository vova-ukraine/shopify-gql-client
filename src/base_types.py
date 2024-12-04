import sys
import re
from abc import ABC, abstractmethod
from typing import Generic
import importlib

from scalars.base import Base

from typing import TypeVar, Generic

from utils import camel_to_snake

#from client import ShopifyGraphQLClient

import logging

logger = logging.getLogger(__name__)

from utils import get_class_by_meta

from exceptions import ValidationError, InvlidArgument, NotEnoughtArguments
from utils import dynamic_import

ObjectT = TypeVar('ObjectT')

# TODO: Parse lists of values
# TODO: Parse nullable
# TODO: Warning on deprecated
class BaseType(ABC):

    # WORKAROUND: Currently we dont check clould the type be nullable
    # Recactor this code to checking None values before creating an instance
    def __new__(cls, value, *args, **kwargs):
        if value is None:
            return None
        return super().__new__(cls)

class ObjectType(BaseType):
    class Fields:
        pass

    # TODO: Check acceess to unpopulated and deprecated fields
    def __init__(self, data: dict) -> None:
        for field_name in data:
            snake_case_field_name = camel_to_snake(field_name)
            if snake_case_field_name in self.Fields.__dict__:
                field = self.Fields.__dict__[snake_case_field_name]
                field_type_class = field.type_loader.get_type_class(field.type_name)
                # handle if data is a list
                field_data = data[field_name]
                if isinstance(field_data, list):
                    value = [field_type_class(item) for item in field_data]
                else:
                    value = field_type_class(field_data)
                logger.debug(f"Setting {snake_case_field_name} (type: {field_type_class}) to {value}")
                setattr(self, snake_case_field_name, value)


class ScalarType(BaseType):
    # Return validated value
    def __new__(cls, value: str) -> str:
        # WORKAROUND: Currently we dont check clould the type be nullable
        # Recactor this code to checking None values before creating an instance
        if value is None:
            return None
        logger.debug(f"Validating {value} (type: {cls.__name__})")
        return cls.validate(value)

    @classmethod
    def validate(cls, value):
        return value
    
class EnumType(ScalarType):

    @classmethod
    def validate(cls, value):
        if value not in cls.__dict__:
            raise ValidationError(f"Invalid Enum value: {value}")
        return value

class InterfaceType(BaseType):
    possible_type_loaders = {}

    def __new__(cls, data: dict) -> BaseType:
        if data["__typename"] in cls.possible_type_loaders:
            required_type_class = cls.possible_type_loaders[data["__typename"]].get_type_class(data["__typename"])
            return required_type_class(data)
        else:
            raise ValueError(f"Invalid type: {data['__typename']}")


class UnionType(InterfaceType):
    possible_type_loaders = {}


    

