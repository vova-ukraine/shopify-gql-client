import keyword
import logging

from utils import camel_to_snake, snake_to_camel

logger = logging.getLogger(__name__)

class BaseGenerator:
    # Should be set in subclasses
    kind_name: str = None
    kind_dir_name: str = None

    # Populated in __init__
    types_data: list[dict] = []
    output_dir: str = None
    schema: dict = None

    # Optional
    ignored_types: list[str] = []

    def __init__(self, schema: dict, output_dir: str):
        self.schema = schema
        self.output_dir = output_dir
        types = schema["types"]
        self.types_data = [t for t in types if t["kind"] == self.kind_name]

    def generate(self):
        for type_data in self.types_data:
            if type_data["name"] in self.ignored_types:
                continue
            class_code = self._generate_class_code(type_data)
            file_name = camel_to_snake(type_data["name"])
            file_name = self._normalize_identifier(file_name)
            with open(f"{self.output_dir}/{self.kind_dir_name}/{file_name}.py", "w") as f:
                f.write(class_code)

    def _generate_class_code(self, type_data: dict):
        raise NotImplementedError()
    
    def _get_field_kind_and_type(self,field_type: dict):
        listed_type = field_type["kind"] == "LIST"
        if "ofType" in field_type and field_type["ofType"] is not None:
            kind, name, listed_type_inside = self._get_field_kind_and_type(field_type["ofType"])
            return kind, name, listed_type or listed_type_inside
        return snake_to_camel(field_type["kind"].lower()), field_type["name"], listed_type
    
    @staticmethod
    def _normalize_identifier(identifier: str):
        snake_identifier = camel_to_snake(identifier)
        if not identifier.isidentifier() or keyword.iskeyword(identifier) \
            or not snake_identifier.isidentifier() or keyword.iskeyword(snake_identifier):
            logger.warning(f"Identifier \"{identifier}\" is not a valid identifier. Replacing with \"_{identifier}\"")
            return f"_{identifier}"
        return identifier
