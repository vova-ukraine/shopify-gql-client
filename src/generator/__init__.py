import json
from generator.enum import EnumGenerator
from generator.object import ObjectGenerator
from generator.interface import InterfaceGenerator
from generator.union import UnionGenerator
from generator.scalar import ScalarGenerator


def generate(schema_filename: str, output_dir_path: str):
    schema = json.load(open(schema_filename))

    scalar_generator = ScalarGenerator(schema["data"]["__schema"], output_dir_path)
    scalar_generator.generate()

    enum_generator = EnumGenerator(schema["data"]["__schema"], output_dir_path)
    enum_generator.generate()

    object_generator = ObjectGenerator(schema["data"]["__schema"], output_dir_path)
    object_generator.generate()

    interface_generator = InterfaceGenerator(schema["data"]["__schema"], output_dir_path)
    interface_generator.generate()  

    union_generator = UnionGenerator(schema["data"]["__schema"], output_dir_path)
    union_generator.generate()

#generate("./schema.json", "./schema")
