import re
import os
import json
import mysql.connector
from web3 import Web3, HTTPProvider
from translate_sql_to_blc import expression_extract
from table_hash_generate import hash_extract_func
from revert_blc_generate import revert_transformer 
from update_prev_val_fetch import prev_val_extract

def contract_instance():
    blockchain_address = 'http://127.0.0.1:9545'

    web3 = Web3(HTTPProvider(blockchain_address))
    acc = web3.eth.accounts[0]
    web3.eth.defaultAccount = acc
    
    compiled_contract_path = 'build/contracts/RBMig.json'
    deployed_contract_address = '0x81d67C3696af36cD832fE97A2d4E65E50688b5e6'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    return contract, acc
  

def sql_connection():
    database = "ZEROPILOTLR"
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
    for sql_statement in content.split("\n"):
        #equivalent blockchain
        equivalent_blc = expression_extract(sql_statement, table_schema_dict)
        transformed_blc = equivalent_blc[:-1] + ",True)"
        temp_split = equivalent_blc.split("(",1)
        func_name = temp_split[0]
        params = temp_split[1].rstrip(")")
        prev_val_exp = prev_val_extract(sql_statement,table_schema_dict)
        
        if prev_val_exp != "":
            temp_cursor  = connection.cursor(buffered=True)
            temp_cursor.execute(prev_val_exp)
            fetched_prev_val = temp_cursor.fetchone()[0]
        #execute DBMS
        cursor.execute(sql_statement)
        #update table hash
        blc_hash = contract.functions.getHash().call({'from': acc})
        print(blc_hash.hex())
        hash_match = blc_hash == bytes(curr_hash)
        if not hash_match:
            # not hash_match
            if show_logs:
                print("Initial #check failed")
            continue
        else:
            if show_logs:
                print("Initial #check passed")
                
        prev_hash = curr_hash
        curr_hash  = hash_extract_func(func_name, params, table_schema_dict,curr_hash)
        revert_func = revert_transformer(func_name, params, table_schema_dict, fetched_prev_val)
        blc_hash = contract.functions.getHash().call({'from': acc})
        if show_logs:
            print(sql_statement)
            print(f'prev blc #: {blc_hash.hex()}')
            print(f'curr table#: {curr_hash.hex()}')
            #print(f'equi blc: {equivalent_blc}')
            print(f'transformed blc: {transformed_blc}')
            print(f'revert func: {revert_func}')
            if prev_val_exp!= "":
                print(f'prev val exp: {prev_val_exp}')
                print(f'fetched prev val: {fetched_prev_val}')
        blc_to_exe = "contract.functions." + transformed_blc + ".transact({'from': acc})"
        #run blockchain
        blc_op = eval(blc_to_exe)
        try:
            blc_hash = contract.functions.getHash().call({'from': acc})    
        except Exception as e:
            print(f"ERROR {e}") 
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
            curr_hash = prev_hash
            # revert blc txn
            blc_to_exe = "contract.functions." + revert_func + ".transact({'from': acc})"
            blc_op = eval(blc_to_exe)
            temp_txn = contract.functions.revertHash().transact({'from': acc})
            blc_hash = contract.functions.getHash().call({'from': acc})
            if show_logs:
                print("Reverted")
                print(f'curr table#: {curr_hash.hex()}')
                print(f'curr blc#: {blc_hash.hex()}')
                print("\n---------\n")

    
if __name__ == "__main__":
    table_schema_dict = read_dict_file()
    read_sync_file(table_schema_dict)
