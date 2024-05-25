import re
import os
import json
import mysql.connector
from web3 import Web3, HTTPProvider, eth
from translate_sql_to_blc import expression_extract
from table_hash_generate import hash_extract_func
from revert_blc_generate import revert_transformer 
from update_prev_val_fetch import prev_val_extract

def gas_used_extract(web3_ins, tx_hash, logs_flag ,txn_type="Hash"):
    tx_receipt = web3_ins.eth.get_transaction_receipt(tx_hash)
    gas = tx_receipt.cumulativeGasUsed
    if logs_flag:
        print(f'Gas used in {txn_type}: {gas}')
    return gas

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
     
    gas_dict = {}
    txn_count_dict = {}
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
        try:
            total_gas = 0
            #equivalent blockchain
            equivalent_blc = expression_extract(sql_statement, table_schema_dict)
            transformed_blc = equivalent_blc[:-1] + ",True)"
            temp_split = equivalent_blc.split("(",1)
            func_name = temp_split[0]
            params = temp_split[1].rstrip(")")
            prev_val_exp = prev_val_extract(sql_statement,table_schema_dict)
            if prev_val_exp != "":
                print(prev_val_exp)
                temp_cursor  = connection.cursor(buffered=True)
                temp_cursor.execute(prev_val_exp)
                fetched_prev_val = temp_cursor.fetchone()[0]
            blc_hash = contract.functions.getHash().call({'from': acc})
            tx_hash = contract.functions.getHash().transact({'from': acc})
            total_gas += gas_used_extract(web3, tx_hash, show_logs)
            # tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
            # gas = tx_receipt.cumulativeGasUsed
            # if show_logs:
            #     print(f'Gas used: {gas}')
            hash_match = blc_hash == bytes(curr_hash)
            if not hash_match:
                # not hash_match
                if show_logs:
                    print("Initial #check failed")
                continue
            else:
                if show_logs:
                    print("Initial #check passed")
            #execute DBMS
            cursor.execute(sql_statement)        
        except Exception as exp:
            # No effect on db till or db effect will be revert because commit❌, TH 🦺safe
            # TH is same
            if show_logs:
                print(f"⚠️{exp}")
            continue              
        try: 
            #table_hash update
            prev_hash = curr_hash    
            curr_hash  = hash_extract_func(func_name, params, table_schema_dict,curr_hash)
        except Exception as exp:
            # DB txn✅, issue with TH update, commit❌, TH🦺
            if show_logs:
                print(f"⚠️{exp}")
            raise Exception("Error updating Table Hash")                        
        blc_hash = contract.functions.getHash().call({'from': acc})
        tx_hash = contract.functions.getHash().transact({'from': acc})
        total_gas += gas_used_extract(web3, tx_hash, show_logs)
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
        try:
            blc_op = eval(blc_to_exe)
            tx_hash = contract.functions.getHash().transact({'from': acc})
            total_gas += gas_used_extract(web3, tx_hash, show_logs,"Operation")

        except Exception as exp:
            # DB txn✅, issue with TH update, commit❌, TH✍️, BLC func❌, ToDo Reset TH 🔁
            if show_logs:
                print(f"⚠️{exp}")
                curr_hash = prev_hash
            continue                        
        
        try:
            blc_hash = contract.functions.getHash().call({'from': acc})
            tx_hash = contract.functions.getHash().transact({'from': acc})
            total_gas += gas_used_extract(web3, tx_hash, show_logs)  
            op_type = sql_statement.split(" ")[0]
            if op_type in gas_dict:
                gas_dict[op_type] = gas_dict[op_type] + total_gas
            else:
                gas_dict[op_type]  = total_gas
            if op_type in txn_count_dict:
                txn_count_dict[op_type] = txn_count_dict[op_type] + 1
            else:
                txn_count_dict[op_type] = 1
            
            if show_logs:
                print(f"Total gas: {total_gas}") 
                print(gas_dict)
                
            #from here    
        except Exception as exp:
            # DB txn✅, issue with TH update, commit❌, TH 🦺safe, BLC # fetch❌
            if show_logs:
                print(f"⚠️{exp}")
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
            try:                
                revert_func = revert_transformer(func_name, params, table_schema_dict, fetched_prev_val)
            except Exception as exp:
                # DB txn✅, commit❌, TH✍️, revert func generation⚠️
                if show_logs:
                    print(f"⚠️{exp}")
                raise Exception("Error generating BLC revert function after #mismatch")            
            # no commit db operation will auto rollback after connection close
            try:
                # reset table hash
                curr_hash = prev_hash
            except Exception as exp:
                if show_logs:
                    print(f"⚠️{exp}")
                raise Exception("Error resetting Table Hash")   

            # revert blc txn
            blc_to_exe = "contract.functions." + revert_func + ".transact({'from': acc})"
            try:
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
    print("-*-"*5)
    print(txn_count_dict)            
    print(gas_dict)
    for k,v in txn_count_dict.items():
        gas_per_txn = gas_dict[k]/txn_count_dict[k]
        block_size = 30000000#30Million Eth
        block_time = 5 #in sec
        txn_per_block = block_size//gas_per_txn
        txn_per_sec = txn_per_block//block_time
        print(f'{k}: {gas_per_txn}')
        print(f'block_size: {block_size}, block_time: {block_time}')
        print(f'{k} per sec: {txn_per_sec}')
if __name__ == "__main__":
    table_schema_dict = read_dict_file()
    read_sync_file(table_schema_dict)
