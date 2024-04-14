import ast, json, inspect

import dvmp.iast.iast_converter as iast_converter

def file_to_iast(path):
    with open(path, "r") as f:
        code = f.readlines()

    # remove all lines that are comments, or imports
    code = [line for line in code if not line.startswith("#") and not line.startswith("import") and not line.startswith("from")] 
    code = [line for line in code if line.strip() != ""]
    code = "".join(code)
    tree = ast.parse(code)

    print('-'*100)
    print(ast.dump(tree))
    print('-'*100)

    return tree_to_iast(tree)

def code_to_iast(code):
    tree = ast.parse(code)
    return tree_to_iast(tree)

def tree_to_iast(tree):
    print('-'*100)
    print(ast.dump(tree))
    print('-'*100)
    parsed = []
    for node in tree.body[0].body:
        p = iast_converter.to_iast(node)
        if p is not None:
            parsed.append(p)
        
    return parsed


if __name__ == "__main__":
    import pprint
    parsed = file_to_iast("dvmp/templates/minimum.py")
    for i, l in enumerate(parsed):
        pprint.pprint(json.loads(l.to_json()))