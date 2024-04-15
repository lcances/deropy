import json, ast, inspect

import dvmp.iast as iast
import dvmp.iast.iast_converter as iast_converter


class IfTest(iast.IastNode):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    @classmethod
    def from_python_ast(cls, node):
                
        return cls(
            iast_converter.to_iast(node.test),
            [iast_converter.to_iast(n) for n in node.body],
            [iast_converter.to_iast(n) for n in node.orelse]
        )

    def to_json(self):
        return json.dumps(
            {
                "type": "IfTest",
                "condition": json.loads(self.condition.to_json()),
                "if_body": [json.loads(n.to_json()) for n in self.if_body],
                "else_body": [json.loads(n.to_json()) for n in self.else_body]
            }
        )

    def __repr__(self):
        return f"if {self.condition}:\n  {self.if_body}\nelse:\n  {self.else_body}"