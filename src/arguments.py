
from type_loaders import TypeLoader, ScalarTypeLoader, EnumTypeLoader, ObjectTypeLoader, InputObjectTypeLoader

# TODO: Make argument serializable
class Argument():
    type_loader = TypeLoader

    def __init__(self, type_name: str, not_null=False) -> None:
        self.type_name = type_name
        self.not_null = not_null

    def get_type_class(self):
        return self.type_loader.get_type_class(self.type_name)

class ScalarArgument(Argument):
    type_loader = ScalarTypeLoader

class EnumArgument(Argument):
    type_loader = EnumTypeLoader

class ObjectArgument(Argument):
    type_loader = ObjectTypeLoader

class InputObjectArgument(Argument):
    type_loader = InputObjectTypeLoader
