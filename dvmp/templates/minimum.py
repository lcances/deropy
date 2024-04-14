# Function Initialize() Uint64
# 1 IF EXISTS("owner") == 0 THEN GOTO 10
# 2 STORE("owner", SIGNER())
# 3 STORE("original_owner", 0)
# 10 RETURN 0
# End Function

# Function UpdateCode(code String) Uint64
# 1 IF LOAD("owner") != SIGNER() THEN GOTO 11
# 2 UPDATE_SC_CODE(code)
# 3 RETURN 0
# 11 RETURN 1
# End Function

# // Function AppendCode(code String) Uint64
# // 1 IF LOAD("owner") != SIGNER() THEN GOTO 11
# // 2 APPEND_SC_CODE(code)
# // 3 RETURN 0
# // 11 RETURN 1
# // End Function


from dvmp.python_to_iast import code_to_iast
from dvmp.dast import *

from dvmp.functions.Exists import exists, exists_dero
from dvmp.functions.Load import load, load_dero
from dvmp.functions.Store import store, store_dero
from dvmp.functions.Signer import signer
from dvmp.functions.Return import ret, ret_dero
from dvmp.sc import SmartContract

class Storage:
    # def Initialize(name: str) -> int:
    #     store("owner", signer())
    #     a: int = 0
    #     a = a + 1
    #     store("original_owner", 0)
    #     return 0
    def Initialize(name: str) -> int:
        a = 0

def load_dast(str_func_name, obj):
    return globals()[str_func_name].from_intermediate_ast(obj)

if __name__ == "__main__":
    import inspect, json

    # get the code of the class
    code = inspect.getsource(Storage)
    parsed = code_to_iast(code)
    
    for f in parsed:
        json_function = json.loads(f.to_json())

        func = load_dast(json_function["type"], json_function)
        flatten_func_body = []
        for b in func.body:
            if isinstance(b, list):
                for l in b:
                    flatten_func_body.append(l)
                continue
            flatten_func_body.append(b)
        print(func)

        for i, l in enumerate(flatten_func_body):
            l_dast = load_dast(l["type"], l)
            print(f'{i+1} {l_dast}')

        print(f'End Function')