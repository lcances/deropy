import ast
import inspect
import json

# Let consider a basic assignment with type hint a: int = 0
def one_function():
    a: int = 0

# parse and display the ast of the function
parsed = ast.parse(inspect.getsource(one_function))
print(ast.dump(parsed))

# the definition is the following
"""
AnnAssign(
    target=Name(id='a', ctx=Store()),
    annotation=Name(id='int', ctx=Load()),
    value=Constant(value=0),
    simple=1
)
"""

# intermediate representation
"""
{
  "type": "VariableDeclarationAndAssignment",
  "variable": {
    "name": "A",
    "type": "Uint64"  # Type is not explicitly declared in Python
    "value": 0
    }
"""

# Which will be translated to the following DVM Basic AST
{
  "type": "VariableDeclaration",
  "variable": {
    "name": "a",
    "type": "Uint64"
  },
},
{
    "type": "Assignment",
    "variable": "a",
    "value": 0
}

# Which will be translated to the following DVM Basic AST
# DIM a AS c_uint64
# LET a = 0parsed

    



for node in ast.walk(parsed):
    if isinstance(node, ast.AnnAssign):
        int_ast = VariableDeclarationAndAssignment.from_python_ast(node)

        print(f'{int_ast.to_json()}')

        d_ast_declare = DVariableDeclaration.from_intermediate_ast(json.loads(int_ast.to_json()))
        d_ast_assign = DAssignment.from_intermediate_ast(int_ast.name, int_ast.value)

        print(d_ast_declare)
        print(d_ast_assign)