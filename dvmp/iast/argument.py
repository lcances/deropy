import json, ast, inspect

import dvmp.iast as iast
import dvmp.iast.iast_converter as iast_converter
from dvmp.utils import type_python_to_intermediate


class Argument(iast.IastNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @classmethod
    def from_python_ast(cls, node):
        return cls(node.arg, iast_converter.to_iast(node.annotation))

    def to_json(self):
        return json.dumps(
            {
                "type": "Argument",
                "name": self.name,
                "ntype": json.loads(self.type.to_json())
            }
        )

    def __repr__(self):
        return f"{self.name}: {self.type}"