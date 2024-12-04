import re
import sys
import importlib

def camel_to_snake(name):
    # if its abbreviation (all letters are uppercase), turn it into lowercase
    if name.isupper():
        return name.lower()
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

def snake_to_camel(name):
    # Convert snake cased name to camel cased name
    return "".join(word.capitalize() for word in name.split("_"))


def dynamic_import(module_name):
    return sys.modules[module_name] if module_name in sys.modules else importlib.import_module(module_name)

def get_class_by_meta(type_name: str, package: str):
    snake_case_type = camel_to_snake(type_name)
    module = dynamic_import(f"{package}.{snake_case_type}")
    return getattr(module, type)

