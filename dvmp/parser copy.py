import inspect
import ast
import regex as re

from dvmp.functions.Exists import exists, exists_dero
from dvmp.functions.Store import store, store_dero
from dvmp.functions.Signer import signer, signer_dero
from dvmp.functions.Return import ret, ret_dero
from dvmp.functions.Random import random
from dvmp.sc import SmartContract

def Initialize() -> int:
    if exists("owner") == 0:
        ret(1)
    else:
        ret(0)
    store("owner", "signer")
    store("original_owner", "signer")
    random("100")
    ret(0)



def class_hint_to_dero_type(hint):
    if hint.strip() == "int":
        return 'Uint64'
    if hint.strip() == "str":
        return 'String'
    raise ValueError(f'Unknown type [{hint.strip()}]')

def parse_function(func):
    func_name = func.split("def ")[1].split("(")[0]
    func_parameters = func.split("(")[1].split(")")[0]
    func_return_hint = func.split("->")[1].split(":")[0]
    print(f'func_return_hint [{func_return_hint}]')
    return f'Function {func_name}({func_parameters}) {class_hint_to_dero_type(func_return_hint)}'

def parse_if_block(func_source, block):
    # first line is the if statement
    # third line is the else statement
    # second and fourth should only contain ret

    operators = ["==", "!=", ">", "<", ">=", "<="]

    lines = []
    if_line = block[0]
    condition = if_line.split("if ")[1].split(":")[0]
    left_part, right_part = None, None
    
    for op in operators:
        if op in condition:
            left_part, right_part = condition.split(op)
            break

    if left_part is None or right_part is None:
        raise Exception("Invalid condition")

    if_line = ('IF ' + left_part + ' ' + op + ' ' + right_part)
    if len(block) == 2:
        if_line += ' THEN GOTO ' + str(len(func_source))
        func_source.append(block[1])

    elif len(block) == 4:
        if_line += ' THEN GOTO ' + str(len(func_source))
        if_line += ' ELSE GOTO ' + str(len(func_source) + 1)
        func_source.append(block[1])
        func_source.append(block[3])
    else:
        raise Exception("Invalid if block")
    
    return if_line, func_source

def parse_line(line):
    def get_dvm_function_parameter(line, function_name):
        if "()" in line:
            return []
        
        parameter_list = line.split(function_name + "(")[1].split(")")[0]
        return parameter_list.split(",")

    _line = line.strip()

    if _line.startswith("def"):
        return parse_function(_line)
    if _line.startswith("exists"):
        return exists_dero(*get_dvm_function_parameter(_line, "exists"))
    if _line.startswith("store"):
        return store_dero(*get_dvm_function_parameter(_line, "store"))
    if _line.startswith("signer"):
        return signer_dero(*get_dvm_function_parameter(_line, "signer"))
    if _line.startswith("ret"):
        return ret_dero(*get_dvm_function_parameter(_line, "ret"))

        


def parse_func(func):
    func_source = inspect.getsourcelines(func)[0]
    counter = 0
    lines = []

    while counter < len(func_source):
        line = func_source[counter]

        if line.strip().startswith("#"):
            counter += 1
            continue

        # The if block are special, there are either 2 lines or 4 lines long, no more
        if line.strip().strip().startswith("if"):
            if "else" in func_source[counter + 2]:
                block = func_source[counter:counter + 4]
                if_lines, func_source = parse_if_block(func_source, block)
                lines.append(f'{counter} {if_lines}')
                counter += 4
                continue
            else:
                block = func_source[counter:counter + 2]
                if_lines, func_source = parse_if_block(func_source, block)
                lines.append(f'{counter} {if_lines}')
                counter += 2
                continue
            
        if counter == 0:
            lines.append(f'{parse_line(line.strip())}')
        else:
            lines.append(f'{counter} {parse_line(line.strip())}')

        counter += 1
    
    lines.append("End Function")
    return lines

def find_first_return(func_lines, return_value):
    for line in func_lines:
        if "Function" in line:
            continue

        if f"RETURN {return_value}" in line:
            return line
    return None

def jump_to_goto(func_lines, goto_line_number):
    for line in func_lines:
        if "Function" in line:
            continue

        line_number = int(line.split(" ")[0])
        if line_number == goto_line_number:
            return line


def clean_parsed_function(func_lines):
    idx = 0
    while idx < len(func_lines):
        line = func_lines[idx]

        if "Function" in line:
            idx += 1
            continue

        if "GOTO" in line:
            line_with_goto = line
            # using a regex to find the line number to jump to
            all_goto = re.findall(r'GOTO \d+', line)
            print('all goto', all_goto)

            # find the corresponding RETURN \d+ line
            for goto in all_goto:
                line_number = int(goto.split(" ")[1])
                return_line = jump_to_goto(func_lines, line_number)
                return_value = return_line.split(" ")[2]
                first_return_line = find_first_return(func_lines, return_value)
                first_return_line_number = int(first_return_line.split(" ")[0])

                # replace the GOTO {line_number} with the first_return_line_number
                func_lines[idx] = func_lines[idx].replace(goto, f'GOTO {first_return_line_number}')
            
            # find the first RETURN \d+ line that correspond to return_line
            if return_line is not None:
                for l in func_lines:
                    if l == return_line:
                        print(l)
                        actual_line = l.split(' ')[0]
                        print(f'actual line {actual_line}')
        
        idx += 1
    
    return func_lines

def rewrite_return_block(func_lines):
    # first the first RETURN line
    return_block_start = None
    for i, line in enumerate(func_lines):
        if "RETURN" in line:
            return_block_start = i
            break
    
    if return_block_start is not None:
        first_line = func_lines[return_block_start]
        original_line_number = int(first_line.split(" ")[0])

        return_block = [l[2:] for l in func_lines[return_block_start:-1]]
        return_block = list(set(return_block))
    
        # rewrite lines number to start from original_line_number
        renumbered_return_block = []
        for i, line in enumerate(return_block):
            renumbered_return_block.append(f'{original_line_number + i} {line}')

        # rebuild the function lines using the new renumbered_return_block
        func_lines = func_lines[:return_block_start] + renumbered_return_block + func_lines[-1:]

        return func_lines
    return func_lines


__sc_name__ = "minimum"
sc = SmartContract()

Initialize()
print(sc.storage)
print(sc.gasStorage)
print(sc.gasCompute)

print(f'total gas compute {sum(sc.gasCompute)} / {SmartContract.max_compute_gaz} : {sum(sc.gasCompute) / SmartContract.max_compute_gaz}')
print(f'total gas storage {sum(sc.gasStorage)} / {SmartContract.max_storage_gas} : {sum(sc.gasStorage) / SmartContract.max_storage_gas}')

# func_lines = parse_func(Initialize)
# for l in func_lines:
#     print(l)
# print('-----------------')
# func_lines = clean_parsed_function(func_lines)
# func_lines = rewrite_return_block(func_lines)
# for l in func_lines:
#     print(l)
# print('-----------------')
