from classes import Queryable
from fields import Field

class Query():
    root_field = None
    args = {}
    fields = []

    def __init__(self, args: dict[str, any] = {}, fields: list[Field] = []) -> None:
        self.args = args
        self.fields = fields

    def __str__(self) -> str:
        return str(self.root_field(**self.args)[self.fields])
    
    def send(self, client):
        json_data = client.request(str(self))
        return self.root_field.type(json_data[self.root_field.name])