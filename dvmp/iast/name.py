import json, ast, inspect

import dvmp.iast as iast
import dvmp.iast.iast_converter as iast_converter


class Name(iast.IastNode):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        return cls(node.id)

    def to_json(self):
        return json.dumps(
            {
                "type": "Name",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"{self.value}"