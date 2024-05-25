import mysql.connector
import os

database = "LRZERODB"
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

cursor = connection.cursor()

cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    with open(f"{output_folder}{table_name}_info.txt", "w") as file:
        file.write(f"Table: {table_name}\n")
        cursor.execute(f"SHOW CREATE TABLE {table_name};")
        create_table_statement = cursor.fetchone()[1]
        cursor.execute(f"DESCRIBE {table_name};")
        columns = cursor.fetchall()
        for column in columns:
            file.write(f"  {column[0]} - {column[1]}\n")
            print(f"  {column[0]} - {column[1]}")
        cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
        primary_keys = cursor.fetchall()
        if primary_keys:
            for key in primary_keys:
                file.write(f"  PK - {key[4]}\n")
                print(f"  PK - {key[4]}")
        constraints = [line.strip() for line in create_table_statement.splitlines() if "CONSTRAINT" in line]
        for constraint in constraints:
            file.write(f"  {constraint}\n")
            print(f"  {constraint}")

cursor.close()
connection.close()
