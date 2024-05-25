import re
import os
import json

def is_attrib_string(table_name_lower, attrib_to_update, table_schema_dict):
    show_logs = False
    for col in table_schema_dict[table_name_lower]["col"]:
        if col[0].capitalize() == attrib_to_update:
            if col[1].startswith("varchar"):
                if show_logs:
                    print(f"str found {col[0]}")
                return True
    return False            


def delete_func_translate(func_name, params, table_schema_dict):
    #func_name = "deleteFacultyRecord"
    #params = "1"
    #DELETE FROM Faculty WHERE FacId = 1;
    #func_name = "deleteEmployeeRecord"
    #params = "315"
    #DELETE FROM Employee WHERE EmpId=315;
    show_logs = False
    table_name = ""
    table_name_lower = ""
    pk = ""
    pk_val_to_delete = ""
    delete_sql_statement = ""
    match = re.search(r'([A-Z][a-z]*)(?=[A-Z])', func_name)
    if match:
        table_name = match.group(1)
        table_name_lower = table_name.lower()
    pk = table_schema_dict[table_name_lower]['pk']
    delete_sql_statement += "DELETE FROM " + table_name + " WHERE " + pk + " = " + params + ";"   
    if show_logs:
        print(f"table name: {table_name}")
        print(f"pk: {pk}")
        print(f"pk val to delete: {params}")
        print(delete_sql_statement)
    return delete_sql_statement

def update_func_translate(func_name, params, table_schema_dict):
    #func_name = "updateFacultyFacname"
    #params = "1, 'Dr. Vinod Pathari'"
    #UPDATE Faculty SET Facname = 'Dr. Vinod Pathari' WHERE FacId = 1;
    show_logs = False
    table_name = ""
    table_name_lower = ""
    col_to_change = ""
    val_to_change = ""
    pk_to_update = ""
    pk_val_to_look = ""
    pk = ""
    update_sql_statement = ""
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
    if is_attrib_string(table_name_lower, col_to_change, table_schema_dict):
        val_to_change = "'" + val_to_change + "'"
    pk = pk.capitalize()    
    if is_attrib_string(table_name_lower, pk, table_schema_dict):
        pk_val_to_look = "'" + pk_val_to_look + "'"
    if show_logs:
        print(f"table name: {table_name}")
        print(f"col to change: {col_to_change}")
        print(f"val to change: {val_to_change}")
        print(f"pk: {pk}")
        print(f"pk val to look: {pk_val_to_look}")
    update_sql_statement += "UPDATE "+ table_name + " SET " + col_to_change + " = " + val_to_change
    update_sql_statement += " WHERE "+ pk + " = " + pk_val_to_look +";"
    if show_logs:
        print(update_sql_statement)       
    return update_sql_statement    

 

def create_func_translate(func_name, params, table_schema_dict):
    show_logs = False
    table_name = ""
    table_name_lower = ""
    cols_ls = []
    cols_ls_str = ""
    translated_query = ""
    match = re.search(r'([A-Z][a-z]*)(?=[A-Z])', func_name)
    if match:
        table_name = match.group(1)
        table_name_lower = table_name.lower()
        if show_logs:
            print(f"table name: {table_name}")
    if table_name != "":
        for col in table_schema_dict[table_name_lower]['col']:
            cols_ls.append(col[0])
        cols_ls_str = ", ".join(cols_ls)
        if show_logs:
            print(params)
        translated_query += "INSERT INTO "+ table_name + " ("+cols_ls_str + ") VALUES (" + params + ");"         
    if show_logs:
        print(translated_query)
    return translated_query    

                        

def blc_expression_extract(func_name, params, table_schema_dict):
    #func_name = "createLabEntry"
    #params = "101,'DSA Lab',1"
    show_logs = False
    match = re.search(r'^([a-z]+)(?=[A-Z])', func_name)
    translated_query = ""
    if match:
        func_type = match.group(1)  
        if show_logs:
            print(f"function type: {func_type}")             
        if func_type == "create":
            translated_query = create_func_translate(func_name, params, table_schema_dict) 
        elif func_type == "update":
            translated_query = update_func_translate(func_name, params, table_schema_dict)                 
        elif func_type == "delete":
            translated_query = delete_func_translate(func_name, params, table_schema_dict)                 
    return translated_query 


def read_blc_func_file(table_schema_dict):
    show_logs = False
    word_after_await = ""
    raw_functions_params  = []
    sql_translated_ls = []
    file_path = os.path.join( "input_translate", "blc", "translate_blc_test.txt")
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
            temp_split = line.split("(",1)
            func_name = temp_split[0]
            if temp_split[1].endswith(")"):
                params = temp_split[1].rstrip(')')
                raw_functions_params.append([func_name, params])                 
            if show_logs:
                print(f"params: {params}")
                print(f"function name: {func_name}")
            match = re.search(r'await\s+(\w+)', line)
            #print(line)
            if show_logs:
                print(f"params: {params}")
                print(f"function name: {func_name}")
                    #print(temp_split[1])
    for raw_func, params in raw_functions_params:
        exp_sql = ""
        exp_sql  = blc_expression_extract(raw_func, params, table_schema_dict)
        #print(exp_sql)
        if exp_sql != "":
            sql_translated_ls.append(exp_sql)
            #print(f"-x- {exp_sql}")
    for sql_translated in sql_translated_ls:
        #pass
        print(sql_translated)
        #print(raw_func, params)              


def read_dict_file():
    file_path = os.path.join( "input_translate", "blc", "schema_dict.txt")
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
    #delete_func_translate(table_schema_dict)
    #update_func_translate(table_schema_dict)
    #blc_expression_extract(table_schema_dict)
    