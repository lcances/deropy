import json, ast, inspect

import dvmp.dast as dast
import dvmp.dast.dast_converter as dast_converter


class IfTest:
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    @classmethod
    def from_intermediate_ast(cls, json_iast):
        condition = dast_converter.to_dast(json_iast["condition"])
        if_body = [dast_converter.to_dast(n) for n in json_iast["if_body"]]
        else_body = [dast_converter.to_dast(n) for n in json_iast["else_body"]]
        return cls(condition, if_body, else_body)
    
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
        if self.else_body:
            return f"IF {self.condition} THEN GOTO {self.if_body[0]} ELSE GOTO {self.else_body[0]}"
        return f"IF {self.condition} THEN GOTO {self.if_body[0]}"