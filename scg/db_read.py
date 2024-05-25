import os
import re
import json

output_folder = "output/"


def read_file(file_path):
    """Reads file in file path and returns the content of file
     Args:
        file_path (str): file path
     Returns:
         str: The contents of file in file_path
    """
    with open(file_path, "r") as file:
        content = file.read()
        return content


def extract_information(content):
    """Reads file in file path and returns the content of file
     Args:
        content (str): contents of table schema
     Returns:
         dict: Dictionary of table information after reading content from param
    """
    table_name_pattern = re.compile(r"Table: (.+)")
    table_info = {"table_name": "", "columns": [], "col": [], "for_key_dep_on": []}
    match = table_name_pattern.search(content)
    if match:
        table_info["table_name"] = match.group(1)
        print(table_info["table_name"])
    lines = content.split("\n")
    for line in lines[1:-1]:
        l_stripped = line.strip()
        match = re.match(r"CONSTRAINT `(.+)` FOREIGN KEY \(`(.+)`\) REFERENCES `(.+)` \(`(.+)`\)", l_stripped)
        if l_stripped.startswith("PK - "):
            pk_temp = l_stripped.split(" - ")[-1]
            table_info['pk'] = pk_temp
            print("table pk " + pk_temp)
        elif match:
            col_dep = match.group(2)
            table_dep_on = match.group(3)
            col_dep_on = match.group(4)
            col_dep_str = col_dep + " -> " + table_dep_on + "." + col_dep_on
            print("COL_DEP " + col_dep_str)
            table_info['for_key_dep_on'].append(col_dep_str)
        else:
            print(l_stripped)
            l_mod = l_stripped.split(" - ")
            table_info['col'].append(l_mod)
    print("Final")
    print(table_info)
    return table_info


if __name__ == "__main__":
    file_list = os.listdir(output_folder)
    all_table_info = {}
    all_foreign_keys = set()
    print_table_info = False
    for file_name in file_list:
        file_path = os.path.join(output_folder, file_name)
        if os.path.isfile(file_path):
            file_content = read_file(file_path)
            table_info = extract_information(file_content)
            if print_table_info:
                print("Table Information:")
                print(table_info)
                print("\n" + "=" * 50 + "\n")
            all_table_info[table_info['table_name']] = table_info
    folder_name = 'dict_output'
    file_name = 'schema_dict.txt'
    file_path = os.path.join(folder_name, file_name)
    os.makedirs(folder_name, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(all_table_info, file)
    for k, v in all_table_info.items():
        print(k, v)
