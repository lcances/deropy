import json

from dvmp.utils import type_python_to_intermediate


class VariableDeclarationAndAssignment():
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        return cls(node.target.id, node.annotation.id, node.value.value)
    
    def to_json(self):
        return json.dumps([
             {
                "type": "VariableDeclaration",
                "variable": {
                    "name": self.name,
                    "type": type_python_to_intermediate(self.type),
                }
            },
            {
                "type": "Assignment",
                "name": self.name,
                "value": self.value
            }
        ])
    
    def __repr__(self):
        return f"{self.name}: {self.type} = {self.value}"