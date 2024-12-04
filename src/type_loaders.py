import sys
import importlib

from base_types import BaseType

from utils import camel_to_snake

class TypeLoader():
    PACKAGE = None

    @classmethod
    def get_type_class(cls, type_name) -> BaseType:
        snake_case_type = camel_to_snake(type_name)
        module_name = f"{cls.PACKAGE}.{snake_case_type}"
        module = sys.modules[module_name] if module_name in sys.modules else importlib.import_module(module_name)
        return getattr(module, type_name)        

class ScalarTypeLoader(TypeLoader):
    PACKAGE = "schema.scalars"

class EnumTypeLoader(TypeLoader):
    PACKAGE = "schema.enums"

class ObjectTypeLoader(TypeLoader):
    PACKAGE = "schema.objects"

class InterfaceTypeLoader(TypeLoader):
    PACKAGE = "schema.interfaces"

class UnionTypeLoader(TypeLoader):
    PACKAGE = "schema.unions"

class InputObjectTypeLoader(TypeLoader):
    PACKAGE = "schema.input_objects"
