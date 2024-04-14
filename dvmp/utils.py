def type_python_to_intermediate(python_hint):
    return {
        "int": "number",
        "str": "String"
    }[python_hint]

def type_intermediate_to_dvm(type):
    return {
        "number": "Uint64",
        "String": "String"
    }[type]