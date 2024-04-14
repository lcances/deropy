import json

from dvmp.utils import type_intermediate_to_dvm

class VariableDeclaration():
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @classmethod
    def from_intermediate_ast(cls, json):
        return cls(json["variable"]["name"], type_intermediate_to_dvm(json["variable"]["type"]))
    
    def to_json(self):
        return json.dumps(
            {
                "type": "VariableDeclaration",
                "variable": {
                    "name": self.name,
                    "type": self.type
                }
            }
        )
    
    def __repr__(self):
        return f"DIM {self.name} AS {self.type}"