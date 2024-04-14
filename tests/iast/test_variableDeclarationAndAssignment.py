import unittest
import ast
import json

from dvmp.iast import VariableDeclarationAndAssignment

# Declare and assign a variable of type int
da = ast.parse("a: int = 0")
da_expected = {
  "type": "VariableDeclarationAndAssignment",
  "variable": {
    "name": "a",
    "type": "number",  # Type is not explicitly declared in Python
    "value": 0
    }
}

class TestVariableDeclarationAndAssignment(unittest.TestCase):
    def test_1(self):
        self.assertEqual(type(da.body[0]), ast.AnnAssign)
        
    def test_2(self):
        int_ast = VariableDeclarationAndAssignment.from_python_ast(da.body[0])
        self.assertEqual(da_expected, json.loads(int_ast.to_json()))