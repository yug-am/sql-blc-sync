import re
import os
import json


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


def delete_query_translate(sql_statement, table_schema_dict):
    #sql_statement = "DELETE FROM Employee WHERE EmpId = 315;"
    #sql_statement = "DELETE FROM Faculty WHERE FacId = 1;"
    show_logs = False
    if show_logs:
        print(f"sql statement: {sql_statement}")
    table_name = ""
    table_name_lower = ""
    pk_capitalize = ""
    value_to_delete = ""
    delete_function_name = ""
    delete_function_call = ""
    words = re.split(r'\s+', sql_statement.strip()) 
    if len(words) >= 3: 
        table_name = words[2]
        table_name_lower = table_name.lower()
        pk_capitalize = table_schema_dict[table_name_lower]['pk'].capitalize()
        match = re.search(r'=\s*(\'[^\']+\'|[^;\s]+)', sql_statement)
        if match:
            value_to_delete = match.group(1)
        if show_logs:
            print(f"table name: {table_name}")
            print(f"primary key: {pk_capitalize}")
            print(f"value to delete: {value_to_delete}")
        table_name_formatted = table_name.capitalize()    
        delete_function_name =  "delete"+table_name_formatted+"Record"
        delete_function_call =  delete_function_name + "(" + value_to_delete + ")"
        if show_logs:
            print(delete_function_call) 
    return delete_function_call



def prev_val_update_query_generator(sql_statement, table_schema_dict):
    show_logs = False
    table_name = ""
    attrib_to_update = ""
    value_to_update = ""
    pk_to_update = ""
    params_transformed = ""
    update_function_name = ""
    table_name_lower =  "" 
    update_function_call = ""
    prev_val_sql_statement = ""
    if show_logs:
        print(f"query is: {sql_statement}")
    words = re.split(r'\s+', sql_statement.strip())
    if len(words) >= 2:
        table_name = words[1]  
        table_name_lower = table_name.lower()
    match = re.search(r'SET\s+(\w+)', sql_statement)
    if match:
        attrib_to_update = match.group(1)                
    match = re.search(r'=\s*(\'[^\']+\'|[^;\s]+)', sql_statement)
    if match:
        value_to_update = match.group(1)
    match = re.search(r'=\s*\'?([^;\s]+)\'?(?=[^=]*$)', sql_statement)
    if match:
        pk_to_update = match.group(1)  
    pk_capitalize = table_schema_dict[table_name_lower]['pk'].capitalize()
    pk_to_update = pk_to_update.strip("'")
    if is_attrib_string(table_name_lower, pk_capitalize, table_schema_dict):
        pk_to_update = "'"+pk_to_update+"'"        
    prev_val_sql_statement += "SELECT "+ attrib_to_update + " FROM " + table_name
    prev_val_sql_statement += " WHERE "+ pk_capitalize + " = " + pk_to_update +" LIMIT 1;"
    if show_logs:
        print(f"prev_val_sql_statement: {prev_val_sql_statement}")
    return prev_val_sql_statement



def prev_val_extract(sql_statement,table_schema_dict):
    #sql_statement = "INSERT INTO faculty (FacId, FacName, CSDept) VALUES (1, 'Dr. Vinod P', TRUE);"
    transformed_query = ""
    sql_op = ""
    show_logs= False
    if show_logs:
        print(f"pv sql statement:{sql_statement}")
    if len(sql_statement)>0:
        sql_op = sql_statement.split(' ', 1)[0]
        sql_op_upper = sql_op.upper()
        if sql_op_upper == "UPDATE":
            return prev_val_update_query_generator(sql_statement,table_schema_dict)
        return ""


def read_query_input(content,table_schema_dict):
    transformed_queries  = []
    if content == "":
        return
    content= content.strip("\n")    
    for line in content.split("\n"):
        temp_transformed = prev_val_extract(line, table_schema_dict)
        if temp_transformed != "":
            transformed_queries.append(temp_transformed)
    return transformed_queries        
     
def read_query_file(table_schema_dict):
    transformed_queries  = []
    file_path = os.path.join( "input_translate", "sql", "translate_sql_test.txt")
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
        temp_transformed = prev_val_extract(line, table_schema_dict)
        if temp_transformed != "":
            transformed_queries.append(temp_transformed)
    for query in transformed_queries:
        print(query)              

def read_dict_file():
    file_path = os.path.join( "input_translate", "sql", "schema_dict.txt")
    op_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            op_dict = json.load(file)
    else:
        print(f"The file '{file_path}' does not exist.")
    return op_dict


def wrapper_func(content):
    table_schema_dict = read_dict_file()
    return read_query_input(content,table_schema_dict)
    
if __name__ == "__main__":

    table_schema_dict = read_dict_file()
    read_query_file(table_schema_dict)
    