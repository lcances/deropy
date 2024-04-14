import unittest
import ast
import json

from dvmp.dast import Assignment, Declaration

ida = {
    "type": "VariableDeclarationAndAssignment",
    "variable": {
        "name": "a",
        "type": "number",  # Type is not explicitly declared in Python
        "value": 0,
    },
}

d_expected = {
    "type": "VariableDeclaration",
    "variable": {"name": "a", "type": "Uint64"},
}
a_expected = {"type": "Assignment", "variable": "a", "value": 0}


class TestVariableDeclarationAndAssignement(unittest.TestCase):
    def test_1(self):
        d_ast_declare = Declaration.from_intermediate_ast(ida)
        d_ast_assign = Assignment.from_intermediate_ast(ida)

        self.assertEqual(d_expected, json.loads(d_ast_declare.to_json()))
        self.assertEqual(a_expected, json.loads(d_ast_assign.to_json()))
