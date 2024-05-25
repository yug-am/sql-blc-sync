import re
import os
import json
import csv
from io import StringIO

def is_attrib_string(table_name_lower, attrib_to_update, table_schema_dict):
    show_logs = False
    if show_logs:
        print("is attrib str call")
    for col in table_schema_dict[table_name_lower]["col"]:
        if col[0].capitalize() == attrib_to_update:
            if show_logs:
                print(col[1])
            if col[1].startswith("varchar"):
                return True
    return False            


def delete_func_rollback_generate(func_name, param, table_schema_dict):
    show_logs = False
    table_name = ""
    table_name_lower = ""
    pk = ""
    pk_val_to_delete = ""
    func_name = func_name.replace("delete", "rollbackDelete")
    if show_logs:
        print(f"function: {func_name}")
        print(f"param: {param}")
    revert_delete_statement =   func_name + "(" + param +  ")"
    if show_logs:
        print(revert_delete_statement)
    return revert_delete_statement

def update_func_rollback_generate(func_name, params, table_schema_dict, prev_val):
    show_logs = False
    table_name = ""
    table_name_lower = ""
    col_to_change = ""
    val_to_change = ""
    pk_to_update = ""
    pk_val_to_look = ""
    pk = ""
    pk_change = False
    update_sql_statement = ""
    revert_update_statement = func_name
    match = re.search(r'([A-Z][a-z]*)(?=[A-Z])', func_name)
    if match:
        table_name = match.group(1)
        table_name_lower = table_name.lower()
    match = re.search(r'([A-Z][a-z]*)$', func_name)    
    if match:
        col_to_change = match.group(1)
    match = re.match(r"\s*(?:'([^']+)'|(\d+))\s*,\s*(?:'([^']+)'|(\d+))\s*$", params)
    if match:
        pk_val_to_look = match.group(1) or match.group(2)
        val_to_change = match.group(3) or match.group(4)
    pk = table_schema_dict[table_name_lower]['pk']
    pk_change = pk.lower() == col_to_change.lower()
    if pk_change:
        pk_val_to_look = val_to_change
    revert_update_statement += "('" + pk_val_to_look + "','"+ prev_val +"', False)"   
    if show_logs:
        print(f'revert: {revert_update_statement}')       
    return revert_update_statement    

 

def create_func_rollback_generate(func_name, params, table_schema_dict):
    #assuming first arg is PK
    show_logs = False
    table_name = ""
    table_name_lower = ""
    cols_ls = []
    cols_ls_str = ""
    revert_function = ""
    func_name = func_name.replace("create","delete")
    func_name = func_name.replace("Entry","Record")
    param_file = StringIO(params)
    param_reader = csv.reader(param_file, quotechar="'", skipinitialspace=True)
    pk_param = "'" + next(param_reader)[0].strip() + "'"
    if show_logs:
        print(f"function: {func_name}")
        print(f"pk_param: {pk_param}")    
    revert_function += func_name + "(" + pk_param +  ",False)" #+ params + ")"         
    if show_logs:
        print(revert_function)
    return revert_function    

                        

def revert_transformer(func_name, params, table_schema_dict, prev_val=""):
    #func_name = "createLabEntry"
    #params = "101,'DSA Lab',1"
    show_logs = False
    match = re.search(r'^([a-z]+)(?=[A-Z])', func_name)
    revert_function = ""
    if match:
        func_type = match.group(1)  
        if show_logs:
            print(f"function type: {func_type}")             
        if func_type == "create":
            revert_function = create_func_rollback_generate(func_name, params, table_schema_dict) 
        elif func_type == "update":
            revert_function = update_func_rollback_generate(func_name, params, table_schema_dict, prev_val)                 
        elif func_type == "delete":
            revert_function = delete_func_rollback_generate(func_name, params, table_schema_dict)                 
    return revert_function 


def read_blc_func_file(table_schema_dict):
    show_logs = False
    word_after_await = ""
    raw_functions_params  = []
    revert_func_generated_ls = []
    file_path = os.path.join( "input_blc_revert", "revert_blc_test.txt")
    content = ""
    if os.path.exists(file_path):
        with open(file_path,'r') as file:
            content =  file.read()     
    else:
        print(f"The file '{file_path}' does not exist.")
    if content == "":
        return
    content= content.strip("\n")    
    for line in content.split("\n"):
        if line != "":
            match = re.search(r'await\s+(\w+)', line)
            if match:
                word_after_await = match.group(1)
                line_formatted =  line.split(word_after_await+".", 1)[-1]
                temp_split = line_formatted.split("(",1)
                func_name = temp_split[0]
                if temp_split[1].endswith(")"):
                    params = temp_split[1].rstrip(')')
                    raw_functions_params.append([func_name, params])                 
                if show_logs:
                    print(f"params: {params}")
                    print(f"function name: {func_name}")
                    #print(temp_split[1])
    for raw_func, params in raw_functions_params:
        exp_sql = ""
        exp_sql  = revert_transformer(raw_func, params, table_schema_dict)
        #print(exp_sql)
        if exp_sql != "":
            revert_func_generated_ls.append(exp_sql)
    for revert_func_generated in revert_func_generated_ls:
        print(revert_func_generated)
        #print(raw_func, params)              


def read_dict_file():
    file_path = os.path.join( "input_blc_revert", "schema_dict.txt")
    op_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            op_dict = json.load(file)
    else:
        print(f"The file '{file_path}' does not exist.")
    return op_dict


if __name__ == "__main__":
    table_schema_dict = read_dict_file()
    read_blc_func_file(table_schema_dict)
    #delete_func_rollback_generate(table_schema_dict)
    #update_func_rollback_generate(table_schema_dict)
    #revert_transformer(table_schema_dict)
    