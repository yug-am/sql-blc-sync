import re
import os
import json
import csv
from io import StringIO
from web3 import Web3
import struct 

delimiter = "_x_"

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


def delete_func_table_hash(func_name, param, table_schema_dict, curr_hash):
    show_logs = False
    bytes_to_hash = curr_hash
    table_name = ""
    table_name_lower = ""
    match = re.search(r'([A-Z][a-z]*)(?=[A-Z])', func_name)
    param = param.strip("'")
    if match:
        table_name = match.group(1)
        table_name_lower = table_name.lower().encode('utf-8')
    bytes_to_hash += delimiter.encode('utf-8') + 'del_'.encode('utf-8') + table_name_lower
    bytes_to_hash += param.encode('utf-8')
    if show_logs:
        print(f"{bytes_to_hash}")
    new_hash = Web3.solidity_keccak(['bytes'],[bytes_to_hash])        
    if show_logs:
        print(f"Hashing: {new_hash}")
    return new_hash

def update_func_table_hash(func_name, params, table_schema_dict, curr_hash):
    show_logs = False
    bytes_to_hash = curr_hash
    params = params.strip("\n")
    param_file = StringIO(params)
    param_reader = csv.reader(param_file, quotechar="'", skipinitialspace=True)
    if show_logs:
        #print(curr_hash)
        print(params)
            
    table_name = ""
    table_name_lower = ""
    col_to_change = ""
    match = re.search(r'([A-Z][a-z]*)(?=[A-Z])', func_name)
    if match:
        table_name = match.group(1) 
        table_name_lower = table_name.lower().encode('utf-8')
    match = re.search(r'([A-Z][a-z]*)$', func_name)    
    if match:
        col_to_change = match.group(1).lower().encode('utf-8')
    bytes_to_hash += delimiter.encode('utf-8') + 'up_'.encode('utf-8') + table_name_lower 
    bytes_to_hash += "_".encode('utf-8') + col_to_change
    for param in next(param_reader):
        bytes_to_hash += delimiter.encode('utf-8') + param.encode('utf-8')  
    if show_logs:
        print(f'{bytes_to_hash}')
    new_hash = Web3.solidity_keccak(['bytes'],[bytes_to_hash])    
    return new_hash   

 

def create_func_table_hash(func_name, params, table_schema_dict,curr_hash):
    #assuming first arg is PK
    show_logs = False
    bytes_to_hash = curr_hash
    params = params.strip("\n")
    param_file = StringIO(params)
    param_reader = csv.reader(param_file, quotechar="'", skipinitialspace=True)
    for param in next(param_reader):
        bytes_to_hash += delimiter.encode('utf-8') + param.encode('utf-8')
    if show_logs:
        print(bytes_to_hash)        
    new_hash = Web3.solidity_keccak(['bytes'],[bytes_to_hash])        
    if show_logs:
        print(f"Hashing: {new_hash}")
    return new_hash    

                        

def hash_extract_func(func_name, params, table_schema_dict,curr_hash):
    #func_name = "createLabEntry"
    #params = "101,'DSA Lab',1"
    show_logs = False
    match = re.search(r'^([a-z]+)(?=[A-Z])', func_name)
    new_hash = ""
    if match:
        func_type = match.group(1)  
        if show_logs:
            print(f"function type: {func_type}")             
        if func_type == "create":
            new_hash = create_func_table_hash(func_name, params, table_schema_dict,curr_hash) 
        elif func_type == "update":
            new_hash = update_func_table_hash(func_name, params, table_schema_dict,curr_hash)                 
        elif func_type == "delete":
            new_hash = delete_func_table_hash(func_name, params, table_schema_dict,curr_hash)                 
    return new_hash 


def read_blc_func_file(table_schema_dict,curr_hash):
    show_logs = False
    word_after_await = ""
    raw_functions_params  = []
    hashes_ls = []
    file_path = os.path.join( "input_table_hash", "hash_blc_test.txt")
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
        curr_hash  = hash_extract_func(raw_func, params, table_schema_dict,curr_hash)
        #print(raw_func, params)
        #print(curr_hash.hex())
        hashes_ls.append(curr_hash)
    for hash_here in hashes_ls:
        print(hash_here.hex())
        #print(raw_func, params)              


def read_dict_file():
    file_path = os.path.join( "input_table_hash","schema_dict.txt")
    op_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            op_dict = json.load(file)
    else:
        print(f"The file '{file_path}' does not exist.")
    return op_dict


if __name__ == "__main__":
    curr_hash = b'\x00' * 32
    curr_hash_hex = "9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69"
    curr_hash = bytes.fromhex(curr_hash_hex)
    table_schema_dict = read_dict_file()
    #curr_hash = 
    read_blc_func_file(table_schema_dict,curr_hash)
    