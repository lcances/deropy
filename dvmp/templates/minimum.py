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
import dvmp.dast as dast

from dvmp.functions.Exists import exists, exists_dero
from dvmp.functions.Load import load, load_dero
from dvmp.functions.Store import store, store_dero
from dvmp.functions.Signer import signer
from dvmp.functions.Return import ret, ret_dero
from dvmp.sc import SmartContract

class Storage:
    def Initialize(name: str) -> int:
        if exists("owner") == 0:
            store("owner", signer())
            store("original_owner", 0)
            return 0
        
        a: int = 0
        a = 1 + 1
        store("test", a)
        return 1
        
        
    
    # def Register(bounty: int, size: int, duration: int) -> int:
    #     a: str = 0
    #     a = a / 1000
    #     return 0


def load_dast(str_func_name, obj):
    return globals()[str_func_name].from_intermediate_ast(obj)

if __name__ == "__main__":
    import inspect, json

    # get the code of the class
    code = inspect.getsource(Storage)
    parsed = code_to_iast(code)

    # print('-----')
    # import pprint
    # pprint.pprint(json.loads(parsed[0].to_json()))
    # print('-----')
    
    for f in parsed:
        func_dvm = []


        json_function = json.loads(f.to_json())
        func = load_dast(json_function["type"], json_function)
        flatten_func_body = []
        for b in func.body:
            if isinstance(b, list):
                for l in b:
                    flatten_func_body.append(l)
                continue
            flatten_func_body.append(b)

        i = 0
        while i < len(flatten_func_body):
            b = flatten_func_body[i]

            # If the block is an IfTest
            # 1. Pop and append the if block to the end of the function
            # 2. Replace the if body with a Goto to the end of the function
            # 3. increment the function body size
            # 4. Repeat 1, 2 and 3 with the else block
            if b["type"] == "IfTest":
                if_body = b["if_body"]
                else_body = b["else_body"]

                b["if_body"] = [json.loads(dast.Name(len(flatten_func_body) + 1).to_json())]
                flatten_func_body.extend(if_body)

                if len(else_body) > 0:
                    b["else_body"] = [json.loads(dast.Name(len(flatten_func_body)).to_json())]
                    flatten_func_body.extend(else_body)
            
            i += 1

        import pprint
        pprint.pprint(flatten_func_body)
        
        # print the DVM-BASIC code
        print(func)
        for i, b in enumerate(flatten_func_body):
            print(f'{i+1} {load_dast(b["type"], b)}')
        print(f'End Function\n')
                





        # func_dvm = []
        # if_block = []

        # json_function = json.loads(f.to_json())
        # func = load_dast(json_function["type"], json_function)
        # flatten_func_body = []
        # for b in func.body:
        #     if isinstance(b, list):
        #         for l in b:
        #             flatten_func_body.append(l)
        #         continue
        #     flatten_func_body.append(b)
        # print(func)

        # for i, l in enumerate(flatten_func_body):
        #     l_dast = load_dast(l["type"], l)
        #     print(f'{i+1} {l_dast}')
    

        # print(f'End Function\n')