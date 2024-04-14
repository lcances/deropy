import ast

import dvmp.iast as iast


def to_iast(node):
    # NODE
    if isinstance(node, ast.ClassDef):
        pass

    if isinstance(node, ast.Assign):
        return iast.Assignment.from_python_ast(node)

    if isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            return iast.VariableDeclarationAndAssignment.from_python_ast(node)
    
    if isinstance(node, ast.Call):
        return iast.FunctionCall.from_python_ast(node)
    
    if isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Call):
            return iast.FunctionCall.from_python_ast(node.value)

    if isinstance(node, ast.FunctionDef):
        body = []
        for b in node.body:
            p = to_iast(b)
            if p is not None:
                body.append(p)
        
        return iast.FunctionDef.from_python_ast(node, body)

    if isinstance(node, ast.Return):
        return iast.Return.from_python_ast(node)
    
    # LEAF
    if isinstance(node, ast.Constant):
        return iast.Constant.from_python_ast(node)

    return None