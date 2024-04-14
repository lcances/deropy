import json, ast, inspect

import dvmp.iast as iast
import dvmp.iast.iast_converter as iast_converter


class Return(iast.IastNode):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        return cls(iast_converter.to_iast(node.value))

    def to_json(self):
        return json.dumps(
            {
                "type": "Return",
                "value": json.loads(self.value.to_json())
            }
        )

    def __repr__(self):
        return f"Return {self.value}"