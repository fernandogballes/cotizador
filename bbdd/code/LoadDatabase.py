from Connection import Connection
import os

def load_database():
    print("Create tables:\n")
    create_tables()
    print("\nCreate catalogos:\n")
    insert_catalogos_data()
    print("\nCreate relations:\n")
    insert_relations_tables_data()


def create_tables():
    execute_sql("bbdd/data/tables/")

def insert_catalogos_data():
    folder_path = "bbdd/data/"
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if 'catalogo' in dir_name.lower(): 
                catalog_folder_path = os.path.join(root, dir_name)
                execute_sql(catalog_folder_path)    

def insert_relations_tables_data():
    folder_path = "bbdd/data/"
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
                if sql_queries:
                    success = connect.execute_common_query(sql_queries)
                    if success:
                        print("Consultas SQL ejecutadas correctamente.")
                    else:
                        print("Ocurrió un error al ejecutar las consultas SQL.")

    except Exception as e:
        print(f"Error al ejecutar scripts SQL: {e}")

if __name__ == '__main__':
    load_database()