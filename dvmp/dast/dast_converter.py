import dvmp.dast as dast

def to_dast(json_object: dict):
    if isinstance(json_object, str):
        return json_object
    if json_object["type"] == "FunctionDef":
        return dast.FunctionDef.from_intermediate_ast(json_object)
    elif json_object["type"] == "FunctionCall":
        return dast.FunctionCall.from_intermediate_ast(json_object)
    elif json_object["type"] == "Constant":
        return dast.Constant.from_intermediate_ast(json_object)
    elif json_object["type"] == "Return":
        return dast.Return.from_intermediate_ast(json_object)
    else:
        raise Exception(f"Unknown type: {json_object['type']}")