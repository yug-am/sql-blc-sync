import re
import os
import json
import mysql.connector
from web3 import Web3, HTTPProvider
from translate_blc_to_sql import blc_expression_extract
from table_hash_generate import hash_extract_func
from revert_blc_generate import revert_transformer 
from update_prev_val_fetch import prev_val_extract

def sql_connection():
    database = "LRONEDB"
    host = "localhost"
    user = "root"
    password = "rootpassmysql"
    port = 3306
    output_folder = "output/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    return connection


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
    show_logs = False
    #mysql
    connection = sql_connection()
    cursor = connection.cursor(buffered = True)
    #chain
    #contract,acc = contract_instance()
    blockchain_address = 'http://127.0.0.1:9545'
     
    # Client instance to interact with the blockchain
    web3 = Web3(HTTPProvider(blockchain_address)) 
    acc = web3.eth.accounts[0] 
    web3.eth.defaultAccount = web3.eth.accounts[0]
     
    # Setting the default account (so we don't need 
    #to set the "from" for every transaction call)
     
    # Path to the compiled contract JSON file
    compiled_contract_path = 'build/contracts/RBMig.json'
    deployed_contract_address = '0x81d67C3696af36cD832fE97A2d4E65E50688b5e6'
     
    # load contract info as JSON
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  
         
        # fetch contract's abi - necessary to call its functions
        contract_abi = contract_json['abi']
     
    # Fetching deployed contract reference
    contract = web3.eth.contract(
        address = deployed_contract_address, abi = contract_abi)
     

    cursor = connection.cursor()
    show_logs = True
    transformed_queries = []
    prev_hash = b'\x00' * 32
    curr_hash = b'\x00' * 32
    curr_hash_hex = "9ae276adc4b0080b16d21614fa309b11bb971eea7954f042ed2cbf16e9e52f69"
    #curr_hash = bytes.fromhex(curr_hash_hex)
    temp_transformed = ""
    blc_hash = ""
    file_path = os.path.join("input_sync_sql_blc", "sync_sql_blc_test.txt")
    equivalent_blc = ""
    content = ""
    blc_to_exe = ""
    revert_func = ""
    prev_val_exp = ""
    fetched_prev_val = ""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
    else:
        print(f"The file '{file_path}' does not exist.")
    if content == "":
        return
    content = content.strip("\n")
    for blc_statement in content.split("\n"):
        temp_split = blc_statement.split("(",1)
        func_name = temp_split[0]
        params = temp_split[1].rstrip(')')    
        try:
            #equivalent sql
            equivalent_sql = blc_expression_extract(func_name, params, table_schema_dict)
            transformed_blc = blc_statement[:-1] + ",True)"
            prev_val_exp = prev_val_extract(equivalent_sql,table_schema_dict)        
            if prev_val_exp != "":
                #if show_logs:
                    #print(f'prev val exp: {prev_val_exp}')
                temp_cursor  = connection.cursor(buffered=True)
                temp_cursor.execute(prev_val_exp)
                fetched_prev_val = temp_cursor.fetchone()[0]
            #initial hash check
            blc_hash = contract.functions.getHash().call({'from': acc})
            hash_match = blc_hash == bytes(curr_hash)
            if not hash_match:
                # not hash_match
                if show_logs:
                    print("Initial #check failed")
                continue
            else:
                if show_logs:
                    print("Initial #check passed")     
         
            if show_logs:
                print(blc_statement)
                print(f'prev blc #: {blc_hash.hex()}')
                print(f'equivalent sql: {equivalent_sql}')
                print(f'transformed blc: {transformed_blc}')
                print(f'revert func: {revert_func}')
                if prev_val_exp!= "":
                    print(f'prev val exp: {prev_val_exp}')
                    print(f'fetched prev val: {fetched_prev_val}')
                print(f'curr table#: {curr_hash.hex()}')
                
            blc_to_exe = "contract.functions." + transformed_blc + ".transact({'from': acc})"
            #run blockchain
            blc_op = eval(blc_to_exe)
        except Exception as exp:
            # BLC txn❌
            if show_logs:
                print(f"⚠️{exp}")
            continue        
        try:
            #execute DBMS
            cursor.execute(equivalent_sql)
        except Exception as exp:
            # DB txn✅,  DB commit❌
            if show_logs:
                print(f"⚠️{exp}")
            continue
        try:    
            #update table hash
            prev_hash = curr_hash
            curr_hash  = hash_extract_func(func_name, params, table_schema_dict,curr_hash)
        except Exception as exp:
            # DB txn✅, issue with TH update, db commit❌, TH🦺
            if show_logs:
                print(f"⚠️{exp}")
            raise Exception("Error updating Table Hash")     
        #check table and db # if no match revert
        try:
            blc_hash = contract.functions.getHash().call({'from': acc})    
        except Exception as exp:
            #BLC txn✅DB txn✅, TH✍️, BH fetch❌ 
            if show_logs:
                print(f"⚠️ {exp}")
            raise Exception("Error fetching Chain Hash")
        hash_match = blc_hash == bytes(curr_hash)   
        #flag intentional revert
        #hash_match = False
        if show_logs:
            print(f'curr blc#: {blc_hash.hex()}')
            test_pass = "pass" if hash_match else "fail"
            print('hash match status: '+test_pass)
            print("\n*************\n")
        if hash_match:
            pass
            #commit to table
            #connection.commit()
        else:
            #handle fail case here
            # no commit db operation will auto rollback after connection close
            # reset table hash
            try:    
                revert_func = revert_transformer(func_name, params, table_schema_dict, fetched_prev_val)
            except Exception as exp:
                # DB txn✅, commit❌, TH✍️, revert func generation⚠️
                if show_logs:
                    print(f"⚠️{exp}")
                raise Exception("Error generating BLC revert function after #mismatch")            
            try:
                # reset table hash
                curr_hash = prev_hash
            except Exception as exp:
                if show_logs:
                    print(f"⚠️{exp}")
                raise Exception("Error resetting Table Hash")   
            # revert blc txn
            try:
                blc_to_exe = "contract.functions." + revert_func + ".transact({'from': acc})"
                blc_op = eval(blc_to_exe)
            except Exception as exp:
                #blockchain revert operation function❌
                if show_logs:
                    print(f"⚠️{exp}")
                raise Exception("Error calling blockchain revert function")   
            try:
                temp_txn = contract.functions.revertHash().transact({'from': acc})
            except Exception as exp:
                #blockchain revert hash❌
                if show_logs:
                    print(f"⚠️{exp}")
                raise Exception("Error calling blockchain revert blockchain Hash") 
            blc_hash = contract.functions.getHash().call({'from': acc})
            hash_match = blc_hash == bytes(curr_hash)
            if not hash_match:
                # hash not match
                raise Exception("Table and Blockchain Hashes don't match")
            if show_logs:
                print("Reverted")
                print(f'curr table#: {curr_hash.hex()}')
                print(f'curr blc#: {blc_hash.hex()}')
                print("\n---------\n")

    
if __name__ == "__main__":
    table_schema_dict = read_dict_file()
    read_sync_file(table_schema_dict)
