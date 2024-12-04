from fields import ObjectField

def on(type_name: str, fields: list):
    field = ObjectField(f"... on {type_name.__name__}", type_name.__name__)
    return field[fields]
