from Connection import Connection
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import paths
import NewActivities

def load_database():
    print('Creando base de datos...')
    delete_bbdd()
    create_tables()
    NewActivities.load_initial_data()
    insert_catalogos_data()
    insert_sublimites_franquicias_coberturas()
    print('Base de datos creada y cargada')


def create_triggers():
    trigger_path = paths.DDBB_TRIGGER_PATH
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
    tables_path = paths.DDBB_PATH + "tables/"
    execute_sql(tables_path)

def insert_catalogos_data():  
    folder_path = paths.DDBB_PATH
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if 'catalogo' in dir_name.lower(): 
                catalog_folder_path = os.path.join(root, dir_name)
                execute_sql(catalog_folder_path)    


def insert_sublimites_franquicias_coberturas():
    folder_path = paths.DDBB_PATH
    """ franquicias_path = folder_path + 'insert franquicia_cobertura/inserts franquicia_cobertura.sql'
    sublimites_path = folder_path + 'insert sublimite_cobertura/inserts sublimite_cobertura.sql' """
    franquicias_path = folder_path + 'inserts franquicia_cobertura/'
    sublimites_path = folder_path + 'inserts sublimite_cobertura/'

    execute_sql(franquicias_path)
    execute_sql(sublimites_path)

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
