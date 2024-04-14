import json, ast, inspect

from dvmp.iast import IastNode
from dvmp.utils import type_python_to_intermediate

code = 'store("owner", "signer")'
python_ast = ast.parse(code)

class FunctionDef(IastNode):
    def __init__(self, name, args, body, returns):
        self.name = name
        self.args = args
        self.body = body
        self.returns = returns

    @classmethod
    def from_python_ast(cls, node, body: IastNode):
        returns = node.returns.id if node.returns is not None else None
        return cls(node.name, [arg.arg for arg in node.args.args], body, returns)
    
    def add_to_body(self, node: IastNode):
        self.body.append(node)

    def to_json(self):
        json_body = [json.loads(b.to_json()) for b in self.body]
        return json.dumps(
            {
                "type": "FunctionDef",
                "function": {
                    "name": self.name,
                    "args": self.args,
                    "body": json_body,
                    "returns": type_python_to_intermediate(self.returns)
                }
            }
        )

    def __repr__(self):
        return f"Function {self.name}({', '.join([str(arg) for arg in self.args])}) -> {self.returns}"
    