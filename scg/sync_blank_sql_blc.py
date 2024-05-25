import re
import os
import json
from translate_sql_to_blc import expression_extract
from table_hash_generate import hash_extract_func


def read_dict_file():
    file_path = os.path.join("input_sync_sql_blc", "schema_dict.txt")
    op_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            op_dict = json.load(file)
    else:
        print(f"The file '{file_path}' does not exist.")
    return op_dict

def read_sync_file(table_schema_dict):
    transformed_queries = []
    curr_hash = b'\x00' * 32
    temp_transformed = ""
    file_path = os.path.join("input_sync_sql_blc", "sync_sql_blc_test.txt")
    equivalent_blc = ""
    content = ""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
    else:
        print(f"The file '{file_path}' does not exist.")
    if content == "":
        return
    content = content.strip("\n")
    for line in content.split("\n"):
        #equivalent blockchain
        equivalent_blc = expression_extract(line, table_schema_dict)[:-1]
        equivalent_blc += ",false)"
        temp_split = equivalent_blc.split("(",1)
        func_name = temp_split[0]
        params = temp_split[1].rstrip(")")
        #run DBMS
        #update table hash
        curr_hash  = hash_extract_func(func_name, params, table_schema_dict,curr_hash)
        print(line)
        #run blockchain
        #get table_hash
        #if not match rollback else commit
        #print(func_name, params)
        print(equivalent_blc)
        print(curr_hash.hex())

if __name__ == "__main__":
    table_schema_dict = read_dict_file()
    read_sync_file(table_schema_dict)
