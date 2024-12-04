from abc import ABC, abstractmethod

from arguments import Argument
from classes import Queryable
from exceptions import InvlidArgument, NotEnoughtArguments
from base_types import BaseType

from type_loaders import TypeLoader, ScalarTypeLoader, EnumTypeLoader, ObjectTypeLoader, UnionTypeLoader, InterfaceTypeLoader

import logging

logger = logging.getLogger(__name__)



class Field(TypeLoader):
    type_loader = TypeLoader

    def __init__(self, name: str, type_name: str, arguments: dict[Argument] = {}):
        self.name = name
        self.type_name = type_name
        self.arguments = arguments
        self.argument_values = {}

    """
    Serialization to query field name as a string
    Example: 
        {
            Object.Fields.field -> enables to provide field name in a query
        }
    """    
    def __str__(self):
        return self.get_field_name_query_string()
    
    """
    Serialization of nested fields in a query
    Example:
        {
            Object1.Fields.field[
                Object2.Fields.field1,
                Object2.Fields.field2
            ] -> enables to provide nested fields in a query
        }
    "fields" parameter is a tuple of fields to be nested
    """
    def __getitem__(self, fields):
        # ??
        if not isinstance(fields, (tuple, list)):
            logger.warning(f"Fields of \"{self.name}\" should be a list, probably you forgot to use a comma (,) after a single field. The single field will converted to a list")
            fields = [fields]
        return self.get_nested_fields_query_string(fields)
    
    """
    Populate field with attribute values
    Create and return a new instance of a Field with populated attribute values to avoid race conditions 
    because the first instans is a class static attribute. (E.g. Object1.Fields.field)

    Example:
        {
            Object1.Fields.field(arg1: value1, arg2: value2) -> enables to provide attribute values in a query
        }
    "attribute_values" is a dictionary of attribute values to be populated
    """
    def __call__(self, **attribute_values) -> None:
        return self.get_attribute_values_populated_instance(attribute_values)
    
    def get_field_name_query_string(self):
        return self.name
    
    def get_nested_fields_query_string(self, fields):
        arguemnts_block = self._prepare_arguments_block()
        return f"""{self.name}{arguemnts_block} {{ {" ".join(map(lambda field: str(field), list(fields)))} }}"""
    
    # TODO: convert value name from snake to camel where needed
    def get_attribute_values_populated_instance(self, values: dict[BaseType]):
        new_instance = self.__class__(self.name, self.type_name, self.arguments)
        for value_name in values:
            if value_name not in self.arguments:
                raise InvlidArgument(f"Argument \'{value_name}\" doens't exists in the query \"{self.name}\"")
            argument_type_class = new_instance.arguments[value_name].get_type_class()
            value = argument_type_class(values[value_name])
            new_instance.argument_values[value_name] = value
        return new_instance
    
    def get_type_class(self):
        return self.type_loader.get_type_class(self.type_name)
    
    def _prepare_arguments_block(self):
        query_arguments = set()
        for argument_name in self.arguments:
            if argument_name in self.argument_values:
                argument_value = self.argument_values[argument_name]
                value = f"\"{argument_value}\"" if isinstance(argument_value, str) else argument_value
                query_arguments.add(f"{argument_name}: {value}")
            elif self.arguments[argument_name].not_null:
                raise NotEnoughtArguments(f"Argument \"{argument_name}\" is requere in query \"{self.name}\"")
        return "(" + ", ".join(query_arguments) + ")" if query_arguments else ""
    

class ScalarField(Field):
    type_loader = ScalarTypeLoader

    def get_nested_fields_query_string(self, fields):
        raise Exception(f"Unable to request field \"{self.name}\" of scalar type \"{self.type_name}\" with nested fields")
    

class EnumField(Field):
    type_loader = EnumTypeLoader
    pass


class ObjectField(Field):
    type_loader = ObjectTypeLoader

    def get_field_name_query_string(self):
        raise Exception(f"Unable to request field \"{self.name}\" of object type \"{self.type_name}\" without defined nested fields")
    

class InterfaceField(Field):
    type_loader = InterfaceTypeLoader

    def __getitem__(self, fields: list[Field]):
        # ??
        field_list = list(fields) if isinstance(fields, (tuple)) or not isinstance(fields, list) else fields
        field_list.append("__typename")
        print(field_list)        
        return super().__getitem__(field_list)


class UnionField(InterfaceField):
    type_loader = UnionTypeLoader


class Query:

    def __init__(self, query_string: str, field_name: str, type_name: str, type_loader: TypeLoader):
        self.query_string = query_string
        self.field_name = field_name
        self.type_name = type_name
        self.type_loader = type_loader

    def query(self, client):
        response = client.request([self.query_string])
        return self.type_loader.get_type_class(self.type_name)(response[self.field_name])


class QueryField(ObjectField):
    
    def get_nested_fields_query_string(self, fields):
        query_string = super().get_nested_fields_query_string(fields)
        return Query(query_string, self.name, self.type_name, self.type_loader)




