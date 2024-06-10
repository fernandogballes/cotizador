from Connection import Connection
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import paths
import NewActivities

def load_database():
    print('Creando base de datos...')
    # delete_bbdd()
    create_tables()
    NewActivities.load_initial_data()
    insert_catalogos_data()
    insert_sublimites_franquicias_coberturas()
    print('Base de datos creada y cargada')

def delete_bbdd():
    delete_path = "Sistema/bbdd/tool_querys/delete_drop.sql" # cambiar por ruta en paths
    connect = Connection()
    with open(delete_path, 'r') as sql_file:
        sql_queries = sql_file.read()
        connect.execute_common_query(sql_queries)

def create_tables():
    tables_path = paths.DDBB_PATH + "tables/"
    for filename in os.listdir(tables_path):
        if filename.endswith(".sql"):
            script_path = os.path.join(tables_path, filename)
            execute_sql(script_path)

def insert_catalogos_data():  
    folder_path = paths.DDBB_PATH
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if 'catalogo' in dir_name.lower(): 
                catalog_folder_path = os.path.join(root, dir_name)
                for filename in os.listdir(catalog_folder_path):
                    if filename.endswith(".sql"):
                        script_path = os.path.join(catalog_folder_path, filename)
                        execute_sql(script_path)

def insert_sublimites_franquicias_coberturas():
    folder_path = paths.DDBB_PATH
    franquicias_path = folder_path + 'inserts franquicia_cobertura/'
    sublimites_path = folder_path + 'inserts sublimite_cobertura/'

    for filename in os.listdir(franquicias_path):
        if filename.endswith(".sql"):
            script_path = os.path.join(franquicias_path, filename)
            execute_sql(script_path)

    for filename in os.listdir(sublimites_path):
        if filename.endswith(".sql"):
            script_path = os.path.join(sublimites_path, filename)
            execute_sql(script_path)

def execute_sql(script_path):
    try:
        connect = Connection()
        print(f"Ejecutando consultas SQL desde: {script_path}")
        with open(script_path, 'r') as sql_file:
            sql_queries = sql_file.read()
        connect.execute_common_query(sql_queries)
    except Exception as e:
        print(f"Error al ejecutar scripts SQL desde {script_path}: {e}")

if __name__ == '__main__':
    # create_tables()
    load_database()
