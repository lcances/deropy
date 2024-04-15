def type_python_to_intermediate(python_hint):
    return {
        "int": "number",
        "str": "String"
    }[python_hint]

def type_intermediate_to_dvm(t):
    return {
        "int": "Uint64",
        "number": "Uint64",
        "str": "String",
        "String": "String"
    }[t]