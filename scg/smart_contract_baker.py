import json
import os

def if_update_hash_init_gen():
    # end input)); }
    return """
    if(__uh){
    prev_hash = curr_hash;
    curr_hash =  keccak256(abi.encodePacked(curr_hash,""" 

def if_update_hash_end_gen():
    # end input)); }
    return "));\n}\n"

def bool_update_hash_gen():
    return ", bool __uh"


def mod_string_arg(x):
    if x == 'string':
        return 'string memory'
    return x


def data_type_getter(attrib_dict):
    pk = attrib_dict['pk']
    pk_dt = ""
    for ent, edt in attrib_dict['col']:
        if pk == ent:
            pk_dt = edt
    if "(" in pk_dt:
        pk_dt = pk_dt[:pk_dt.index("(")]
    pk_dt = mod_string_arg(pk_dt)
    return pk_dt


def require_statement_generator(mapping, col, err, bool_val=False):
    bool_here = 'true' if bool_val else 'false'
    req_str = 'require({mapping_name}[_{col_name}].struct_valid_check == {bv}, "{error}");\n'.format(
        mapping_name=mapping, col_name=col, error=err, bv=bool_here)
    return req_str


def fk_const_generator_update_parent(table_name, pk, col, parent_fk_dep):
    fk_gen_str = ""
    col = col.lower()
    pk = pk.lower()
    mapping_str = pk + table_name.capitalize() + "Mapping"
    if table_name in parent_fk_dep:
        if col in parent_fk_dep[table_name]:
            fk_gen_str += "require(" + parent_fk_dep[table_name][
                col] + "[_" + pk + "] == 0" + ', "FK dependency violation");\n'
    return fk_gen_str


def fk_const_generator_update_child(table_name, pk, col, child_fk_dep):
    fk_gen_str = ""
    mapping_str = pk + table_name.capitalize() + "Mapping"
    if table_name in child_fk_dep:
        if col in child_fk_dep[table_name]:
            fk_gen_str += child_fk_dep[table_name][col] + "[_" + col + "] += 1;\n"
            fk_gen_str += child_fk_dep[table_name][col] + "[" + mapping_str + "[_" + pk + "]." + col + "] -= 1;\n"
    return fk_gen_str


def update_pk_func_baker(table_name, pk, pk_dt, col, col_dt, parent_fk_dep, child_fk_dep):
    pk = pk.lower()
    col = col.lower()
    fn_str = "function update" + table_name.capitalize() + col.capitalize() + "("
    col += "_new"
    ls_arg = [[mod_string_arg(pk_dt), "_" + pk], [mod_string_arg(col_dt), "_" + col]]
    fn_str += ",".join([" ".join(k) for k in ls_arg])
    fn_str += bool_update_hash_gen() + ") external {\n"
    mapping_str = pk + table_name.capitalize() + "Mapping"
    fn_str += require_statement_generator(mapping_str, pk, "PK not found", True)
    fn_str += require_statement_generator(mapping_str, col, "new PK exists", False)
    fn_str += fk_const_generator_update_child(table_name, pk, pk, child_fk_dep)
    fn_str += fk_const_generator_update_parent(table_name, pk, pk, parent_fk_dep)
    fn_str += mapping_str + "[_" + col + "] = " + mapping_str + "[_" + pk + "];\n"
    fn_str += mapping_str + "[_" + col + "]." + pk + " = _" + col + ";\n"
    fn_str += mapping_str + "[_" + pk + "].struct_valid_check" + " = false;\n"
    fn_str += if_update_hash_init_gen()
    fn_str += " '_x_', 'up_"+ table_name +"_"+pk+"',"    
    hash_ip_ls = []
    hash_ip_str = "'_x_' ,"
    for col in [pk, col]:
        hash_ip_ls.append("_"+col)       
    hash_ip_str += " , '_x_' , ".join(hash_ip_ls)
    fn_str += hash_ip_str
    fn_str += if_update_hash_end_gen()    
    fn_str += "}\n"
    return fn_str


def update_func_baker(table_name, pk, pk_dt, col, col_dt, parent_fk_dep, child_fk_dep):
    pk = pk.lower()
    col = col.lower()
    fn_str = "function update" + table_name.capitalize() + col.capitalize() + "("
    ls_arg = [[mod_string_arg(pk_dt), "_" + pk], [mod_string_arg(col_dt), "_" + col]]
    fn_str += ",".join([" ".join(k) for k in ls_arg])
    fn_str += bool_update_hash_gen() + ") external {\n"
    mapping_str = pk + table_name.capitalize() + "Mapping"
    fn_str += require_statement_generator(mapping_str, pk, "Attrib not found", True)
    fn_str += fk_const_generator_update_child(table_name, pk, col, child_fk_dep)
    fn_str += fk_const_generator_update_parent(table_name, pk, col, parent_fk_dep)
    fn_str += mapping_str + "[_" + pk + "]." + col + "=_" + col + ";"
    fn_str += if_update_hash_init_gen()    
    #update imp
    fn_str += " '_x_', 'up_"+ table_name +"_"+col+"',"
    hash_ip_ls = []
    hash_ip_str = "'_x_' ,"
    for col in [pk, col]:
        hash_ip_ls.append("_"+col)       
    hash_ip_str += " , '_x_' , ".join(hash_ip_ls)
    fn_str += hash_ip_str
    fn_str += if_update_hash_end_gen()    
    fn_str += "}\n"
    return fn_str


def view_rec_gen(table_name, table_dict, struct_transform_dict):
    pk = table_dict['pk'].lower()
    pk_dt = mod_string_arg(struct_transform_dict[data_type_getter(table_dict)])
    fn_str = "function view" + table_name.capitalize() + "Record("
    fn_str += pk_dt + " _" + pk + ")" + "external view returns" + "("
    for col, col_dt in table_dict['col']:
        col = col.lower()
        if "(" in col_dt:
            col_dt = col_dt[:col_dt.index("(")]
        fn_str += mod_string_arg(struct_transform_dict[col_dt]) + " " + col + ", "
    fn_str = fn_str[:-2]
    fn_str += "){\n"
    mapping_str = pk + table_name.capitalize() + "Mapping"
    fn_str += require_statement_generator(mapping_str, pk, "PK not found", True)
    for col, col_dt in table_dict['col']:
        col = col.lower()
        fn_str += col + "=" + mapping_str + "[_" + pk + "]" + "." + col + ";\n"
    fn_str += "}\n"
    return fn_str


def fk_const_generator_del_child(table_name, pk, col, child_fk_dep):
    fk_gen_str = ""
    mapping_str = pk + table_name.capitalize() + "Mapping"
    if table_name in child_fk_dep:
        for cv in child_fk_dep[table_name]:
            fk_gen_str += child_fk_dep[table_name][cv] + "[" + mapping_str + "[_" + pk + "]." + cv + "] -= 1;\n"
    return fk_gen_str

def fk_const_generator_roll_del_child(table_name, pk, col, child_fk_dep):
    fk_gen_str = ""
    mapping_str = pk + table_name.capitalize() + "Mapping"
    if table_name in child_fk_dep:
        for cv in child_fk_dep[table_name]:
            fk_gen_str += child_fk_dep[table_name][cv] + "[" + mapping_str + "[_" + pk + "]." + cv + "] += 1;\n"
    return fk_gen_str


def del_func_baker(table_name, attrib_dict, struct_transform_dict, parent_fk_dep, child_fk_dep):
    fn_str = ""
    pk = attrib_dict['pk'].lower()
    pk_dt = mod_string_arg(struct_transform_dict[data_type_getter(attrib_dict)])
    #pk_dt = data_type_getter(attrib_dict)
    if "(" in pk_dt:
        pk_dt = pk_dt[:pk_dt.index("(")]
    mapping_str = pk + table_name.capitalize() + "Mapping"
    fn_str = "function delete" + table_name.capitalize() + "Record("
    fn_str += pk_dt + " _" + pk + bool_update_hash_gen() + ")" + "external " + "{\n"
    fn_str += require_statement_generator(mapping_str, pk, "PK not found", True)
    fn_str += fk_const_generator_update_parent(table_name, pk, pk, parent_fk_dep)
    fn_str += fk_const_generator_del_child(table_name, pk, pk, child_fk_dep)
    fn_str += mapping_str + "[_" + pk + "].struct_valid_check" + " = false;\n"
    fn_str += if_update_hash_init_gen()    
    fn_str += " '_x_', 'del_"+ table_name +"',_"+pk
    fn_str += if_update_hash_end_gen()    

    fn_str += "}\n"
    return fn_str

def rollback_del_func_baker(table_name, attrib_dict, struct_transform_dict, parent_fk_dep, child_fk_dep):
    fn_str = ""
    pk = attrib_dict['pk'].lower()
    pk_dt = mod_string_arg(struct_transform_dict[data_type_getter(attrib_dict)])
    #pk_dt = data_type_getter(attrib_dict)
    if "(" in pk_dt:
        pk_dt = pk_dt[:pk_dt.index("(")]
    mapping_str = pk + table_name.capitalize() + "Mapping"
    fn_str = "function rollbackDelete" + table_name.capitalize() + "Record("
    fn_str += pk_dt + " _" + pk + ")" + "external " + "{\n"
    fn_str += fk_const_generator_roll_del_child(table_name, pk, pk, child_fk_dep)
    fn_str += mapping_str + "[_" + pk + "].struct_valid_check" + " = true;\n"
    fn_str += "}\n"
    return fn_str

def update_func_generator(table_name, attrib_dict, struct_transform_dict, parent_fk_dep, child_fk_dep):
    upf_str = ""
    pk = attrib_dict['pk']
    pk_dt = data_type_getter(attrib_dict)
    for col_pair in attrib_dict['col']:
        col, data_type = col_pair
        if "(" in data_type:
            data_type = data_type[:data_type.index("(")]
        if pk == col:
            upf_str += update_pk_func_baker(table_name, pk, struct_transform_dict[pk_dt], col,
                                            struct_transform_dict[data_type], parent_fk_dep, child_fk_dep)
        else:
            upf_str += update_func_baker(table_name, pk, struct_transform_dict[pk_dt], col,
                                         struct_transform_dict[data_type], parent_fk_dep, child_fk_dep)
    return upf_str


def for_key_decoder(fk_dep):
    table_name, col = fk_dep.split(".")
    val = col + table_name.capitalize() + "FkMapping"
    return val


def for_ct_decoder(fk_dep):
    table_name, col = fk_dep.split(".")
    val = col + table_name.capitalize() + "FkCtMapping"
    return val


def require_statment_am_generator(mapping, col, dep_key, err, bool_val=False):
    bool_here = 'true' if bool_val else 'false'
    req_str = 'require({mapping_name}[_{dk}].{col_name} == _{dk}, "{error}");'.format(mapping_name=mapping,
                                                                                      col_name=col, error=err,
                                                                                      bv=bool_here, dk=dep_key)
    return req_str


def func_from_dict(str_dict, pk_dict, fk_dep, fk_on_dict):
    func_init_str = ""
    for table_name, content in str_dict.items():
        table_name_formatted = table_name.capitalize()
        func_init_str += "\nfunction create" + table_name_formatted + "Entry(\n"
        params_list = ", ".join([mod_string_arg(entry[0]) + " _" + entry[1] for entry in content])
        func_init_str += params_list + bool_update_hash_gen() + ") external {\n"
        func_dep_ct = ""
        func_init_str += require_statement_generator(pk_dict[table_name_formatted] + table_name_formatted + "Mapping",
                                                     pk_dict[table_name_formatted], "PK not unique")
        if table_name.lower() in fk_dep:
            for col_dep_t, fk in fk_dep[table_name].items():
                for_map_dep = for_key_decoder(fk)
                for_ct_map_dep = for_ct_decoder(fk)
                func_dep_ct += for_ct_map_dep + "[_" + col_dep_t + "] += 1;\n"
                z_temp = require_statement_generator(for_map_dep,
                                                     col_dep_t, True, "FK ref not found")
                func_init_str += func_dep_ct

        temp_pk_here = pk_dict[table_name_formatted]
        temp_struct_map = ""
        func_init_str += "\n"
        temp_map_here = temp_pk_here + table_name_formatted + "Mapping"
        temp_struct_map += temp_map_here + "[_" + temp_pk_here + "]=" + table_name_formatted + "({"
        map_args_list = ",\n".join([entry[1] + ": _" + entry[1] for entry in content])
        map_args_list += ",\nstruct_valid_check:true"
        func_init_str += temp_struct_map
        func_init_str += map_args_list
        func_init_str += "});\n"
        if table_name in fk_on_dict:
            for col in fk_on_dict[table_name]:
                temp_str_fk_on = col + table_name_formatted + "FkMapping" + "[_" + col + "]=" + col + table_name_formatted + "Mapping" + "[_" + col + "];\n"
                func_init_str += temp_str_fk_on
        func_init_str += if_update_hash_init_gen()
        hash_ip_ls = []
        hash_ip_str = "'_x_' ,"
        for dt, col in struct_dict[table_name]:
            hash_ip_ls.append("_"+col)       
        hash_ip_str += " , '_x_' , ".join(hash_ip_ls)
        func_init_str += hash_ip_str
        func_init_str += if_update_hash_end_gen()
        #print(hash_ip_str)
        func_init_str += "\n}\n"
    return func_init_str


def table_attr_name(table, attrib):
    table.capitalize() + "." + attrib


def struct_from_dict(str_dict):
    struct_init_str = ""
    for table_name, content in str_dict.items():
        struct_init_str += "struct " + table_name.capitalize() + "{\n"
        for temp_data_type, attb in content:
            attrib_name = attb.lower()
            temp_str = temp_data_type + " " + attrib_name + ";"
            struct_init_str += temp_str + "\n"
        struct_init_str += "bool struct_valid_check;\n"
        struct_init_str += "}\n"
    return struct_init_str


def pk_map_from_dict(pk_dict, attrib_data_type_dict):
    mapping_init_str = ""
    for table_name, pk in pk_dict.items():
        mapping_init_str += "mapping(" + attrib_data_type_dict[
            table_name + "." + pk] + " => " + table_name + ") " + pk + table_name + "Mapping;\n"
    return mapping_init_str


def fk_dep_ct_from_dict(fk_on_dict, attrib_data_type_dict):
    mapping_init_str = ""
    for table_name, dep_cols in fk_on_dict.items():
        table_name = table_name.capitalize()
        for col in dep_cols:
            mapping_init_str += "mapping(" + attrib_data_type_dict[
                table_name + "." + col] + " => uint256) " + col + table_name + "FkCtMapping;\n"
    return mapping_init_str


def fk_dep_on_from_dict(fk_on_dict, attrib_data_type_dict):
    mapping_init_str = ""
    for table_name, dep_cols in fk_on_dict.items():
        table_name = table_name.capitalize()
        for col in dep_cols:
            mapping_init_str += "mapping(" + attrib_data_type_dict[
                table_name + "." + col] + " => " + table_name + ") " + col + table_name + "FkMapping;\n"
    return mapping_init_str

def revert_hash_func_generator():
    return """function revertHash()external {
     curr_hash = prev_hash;
}"""

def return_hash_func_generator():
    return """function getHash() public view returns (bytes32) {
return curr_hash;
    }"""

if __name__ == "__main__":

    show_logs = False
    folder_name = 'dict_output'
    file_name = 'schema_dict.txt'
    file_path = os.path.join(folder_name, file_name)
    curr_struct_str = ""
    struct_dict = {}
    pk_dict = {}
    fk_dep = {}  # requires oth
    fk_dep_on = {}  # should be
    attrib_data_type_dict = {}
    fk_list = []
    struct_transform_dict = {'int': 'int', 'varchar': 'string', 'tinyint': 'bool'}
    data_types_dict = {}
    parent_fk_dep = {}
    child_fk_dep = {}
    update_func = ""
    view_rec_func = ""
    del_rec_func = ""
    roll_del_rec_func = ""
    with open(file_path, 'r') as file:
        loaded_dict = json.load(file)
    for table_name, content in loaded_dict.items():
        if content['for_key_dep_on']:
            fk_dep[table_name] = {}
            for dep in content['for_key_dep_on']:
                temp_dep_split = dep.lower().split(' -> ')
                temp_dep_on = temp_dep_split[1]
                temp_dep = temp_dep_split[0]
                table_fk_dep, attrib_fk_dep = temp_dep_on.split(".")
                parent_fk_dep[table_fk_dep] = {}
                child_fk_dep[table_name] = {}
                temp_ct_mapping_str = attrib_fk_dep + table_fk_dep.capitalize() + "FkCtMapping"
                parent_fk_dep[table_fk_dep][attrib_fk_dep] = temp_ct_mapping_str
                child_fk_dep[table_name][temp_dep] = temp_ct_mapping_str
    for table_name, content in loaded_dict.items():
        struct_dict[table_name] = []
        struct_transform_dict[table_name] = []
        temp_struct_members = []
        temp_str = "struct " + table_name.capitalize() + "{"
        curr_struct_str += temp_str + "\n"
        pk_dict[table_name.capitalize()] = content['pk'].lower()
        if content['for_key_dep_on']:
            fk_dep[table_name] = {}
            for dep in content['for_key_dep_on']:
                temp_dep_split = dep.lower().split(' -> ')
                temp_dep_on = temp_dep_split[1]
                temp_dep = temp_dep_split[0]
                fk_dep[table_name][temp_dep] = temp_dep_on
                table_fk_dep, attrib_fk_dep = temp_dep_on.split(".")
                temp_ct_mapping_str = attrib_fk_dep + table_fk_dep.capitalize() + "FkCtMapping"
                temp_dep_split = temp_dep_on.split(".")
                if temp_dep_split[0] not in fk_dep_on:
                    fk_dep_on[temp_dep_split[0]] = set()
                fk_dep_on[temp_dep_split[0]].add(temp_dep_split[1])
        for col in content['col']:
            temp_data_type = col[1]
            attrib_name = col[0].lower()
            if '(' in temp_data_type:
                temp_data_type = temp_data_type[:temp_data_type.index("(")]
            temp_sol_equi_type = struct_transform_dict[temp_data_type]
            attrib_data_type_dict[table_name.capitalize() + "." + attrib_name] = temp_sol_equi_type
            temp_str = temp_sol_equi_type + " " + attrib_name + ";"
            struct_dict[table_name].append([temp_sol_equi_type, attrib_name])
            curr_struct_str += temp_str + '\n'
        temp_str = "}"
        curr_struct_str += temp_str + '\n'
        if show_logs:
            print(struct_dict[table_name])
        update_func += update_func_generator(table_name, content, struct_transform_dict, parent_fk_dep,
                                             child_fk_dep) + "\n"
        view_rec_func += view_rec_gen(table_name, content, struct_transform_dict)
        del_rec_func += del_func_baker(table_name, content, struct_transform_dict, parent_fk_dep, child_fk_dep)
        roll_del_rec_func += rollback_del_func_baker(table_name, content, struct_transform_dict, parent_fk_dep, child_fk_dep)
        
        
    op = "// SPDX-License-Identifier: GPL-3.0\npragma solidity >=0.8.2 <0.9.0;\ncontract RBMig {\n \n"
    op += "bytes32 curr_hash ;\nbytes32 prev_hash ;\n"
    op += struct_from_dict(struct_dict)
    op += pk_map_from_dict(pk_dict, attrib_data_type_dict)
    op += fk_dep_on_from_dict(fk_dep_on, attrib_data_type_dict)
    op += fk_dep_ct_from_dict(fk_dep_on, attrib_data_type_dict)
    op += func_from_dict(struct_dict, pk_dict, fk_dep, fk_dep_on)
    op += update_func
    op += view_rec_func
    op += del_rec_func
    op += roll_del_rec_func
    op += revert_hash_func_generator()
    op += return_hash_func_generator()
    op += "\n}\n"
    print(op)
