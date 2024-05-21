from Connection import Connection
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import config

def load_database():
    delete_bbdd()
    print("Create tables:")
    create_tables()
    print("\nCreate catalogos:")
    create_triggers()
    insert_catalogos_data()
    print("\nCreate relations:")
    insert_relations_tables_data()

def create_triggers():
    trigger_path = config.DDBB_TRIGGER_PATH
    connect = Connection()
    with open(trigger_path, 'r') as sql_file:
        sql_queries = sql_file.read()
        connect.execute_common_query(sql_queries)

def delete_bbdd():
    delete_path = "Sistema/bbdd/tool_querys/delete_drop.sql"
    connect = Connection()
    with open(delete_path, 'r') as sql_file:
        sql_queries = sql_file.read()
        connect.execute_common_query(sql_queries)


def create_tables():
    tables_path = config.DDBB_PATH + "tables/"
    execute_sql(tables_path)

def insert_catalogos_data():
    folder_path = config.DDBB_PATH
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if 'catalogo' in dir_name.lower(): 
                catalog_folder_path = os.path.join(root, dir_name)
                execute_sql(catalog_folder_path)    

def insert_relations_tables_data():
    folder_path = config.DDBB_PATH
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if 'catalogo' not in dir_name.lower() and 'tables' not in dir_name.lower():  
                catalog_folder_path = os.path.join(root, dir_name)
                execute_sql(catalog_folder_path) 

def execute_sql(folder_path):
    try:
        connect = Connection()
        # Recorrer todos los archivos en la carpeta especificada
        for filename in os.listdir(folder_path):
            if filename.endswith(".sql"):
                script_path = os.path.join(folder_path, filename)
                print(f"Ejecutando consultas SQL desde: {script_path}")

                # Leer el contenido del archivo SQL
                with open(script_path, 'r') as sql_file:
                    sql_queries = sql_file.read()

                # Ejecutar las consultas SQL
                connect.execute_common_query(sql_queries)

    except Exception as e:
        print(f"Error al ejecutar scripts SQL: {e}")

if __name__ == '__main__':
    load_database()
    #print(Connection().execute_select_query("SELECT * FROM catalogo_coberturas;"))