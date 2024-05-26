import pandas as pd
from Connection import Connection
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import paths
from unidecode import unidecode

def select_id_cobertura(nombre_cobertura):
    try:
        connect = Connection()
        query = f"SELECT id_cobertura FROM catalogo_coberturas WHERE nombre_cobertura='{nombre_cobertura}'"
        result = connect.execute_select_query(query)
        id_cobertura = result[0][0] if result else None
    except Exception as e:
        print(f"Error al ejecutar scripts SQL: {e}")
        id_cobertura = None

    return id_cobertura

def select_id_activity(nombre_actividad):
    try:
        connect = Connection()
        query = f"SELECT id_actividad FROM catalogo_actividades WHERE nombre_actividad='{nombre_actividad}'"
        result = connect.execute_select_query(query)
        id_actividad = result[0][0] if result else None
    except Exception as e:
        print(f"Error al ejecutar scripts SQL: {e}")
        id_actividad = None

    return id_actividad

def create_all_actividad_cobertura():
    try:
        connect = Connection()

        # Query para obtener todas las actividades
        activities_query = "SELECT id_actividad, nombre_actividad, agravada_flag FROM catalogo_actividades"
        activities_data = connect.execute_select_query(activities_query)
        activities_columns = ['id_actividad', 'nombre_actividad', 'agravada_flag']
        activities_df = pd.DataFrame(activities_data, columns=activities_columns)

        # Query para obtener todas las coberturas para cada actividad
        cobertura_query = """
            SELECT ca.nombre_actividad, cc.nombre_cobertura, ca.agravada_flag
            FROM catalogo_actividades ca
            JOIN actividad_cobertura ac ON ca.id_actividad = ac.id_actividad
            JOIN catalogo_coberturas cc ON cc.id_cobertura = ac.id_cobertura
            ORDER BY cc.id_cobertura
        """
        cobertura_data = connect.execute_select_query(cobertura_query)
        cobertura_columns = ['nombre_actividad', 'nombre_cobertura', 'agravada_flag']
        cobertura_df = pd.DataFrame(cobertura_data, columns=cobertura_columns)
        coberturas_order= cobertura_df['nombre_cobertura'].drop_duplicates()

        # Pivotar el DataFrame de coberturas para tener una columna por cada tipo de cobertura
        cobertura_pivot = cobertura_df.pivot_table(
            index='nombre_actividad', 
            columns='nombre_cobertura', 
            values='agravada_flag',
            aggfunc=lambda x: 'X', 
            fill_value=''
        ).reset_index()

        # Convertir la columna 'agravada_flag' a 'X' si es True, de lo contrario ''
        activities_df['agravada_flag'] = activities_df['agravada_flag'].apply(lambda x: 'X' if x else '')

        df_agravada = activities_df[['nombre_actividad', 'agravada_flag']]

        # Merge de los DataFrames
        final_df = pd.merge(cobertura_pivot, df_agravada, on='nombre_actividad')

        column_order = ['nombre_actividad'] + coberturas_order.tolist() + ['agravada_flag']
        final_df = final_df[column_order]
        final_df.rename(columns={'agravada_flag': 'AGRAVADO', 'nombre_actividad': 'ACTIVIDADES'}, inplace=True)

        # Guardar el DataFrame en un archivo Excel
        final_df.to_excel(paths.DDBB_MANTENIMIENTO_ACTIVIDADES_ACTUAL, index=False)

        print(f"Archivo Excel creado correctamente en: {paths.DDBB_MANTENIMIENTO_ACTIVIDADES_ACTUAL}")

    except Exception as e:
        print(f"Error al ejecutar las queries o al crear el archivo Excel: {e}")

def insert_activity(nombre_actividad, agravada_flag):
    try:
        connect = Connection()
        query = f"""
            INSERT INTO catalogo_actividades (nombre_actividad, agravada_flag)
            VALUES ('{nombre_actividad}', {agravada_flag})
        """
        result = connect.execute_common_query(query)
        return result[0][0] if result else None
    except Exception as e:
        print(f"Error al insertar actividad: {e}")
        return None

def insert_cobertura(nombre_cobertura):
    try:
        connect = Connection()
        query = f"""
            INSERT INTO catalogo_coberturas (nombre_cobertura)
            VALUES ('{nombre_cobertura}')
        """
        result = connect.execute_common_query(query)
        return result[0][0] if result else None
    except Exception as e:
        print(f"Error al insertar cobertura: {e}")
        return None

def insert_actividad_cobertura(id_actividad, id_cobertura):
    try:
        connect = Connection()
        query = f"""
            INSERT INTO actividad_cobertura (id_actividad, id_cobertura)
            VALUES ({id_actividad}, {id_cobertura})
        """
        connect.execute_common_query(query)
    except Exception as e:
        print(f"Error al insertar actividad_cobertura: {e}")


def update_database_with_new_data():
    try:
        # Leer el archivo actual y el actualizado
        current_df = pd.read_excel(paths.DDBB_MANTENIMIENTO_ACTIVIDADES_ACTUAL)
        updated_df = pd.read_excel(paths.DDBB_MANTENIMIENTO_ACTIVIDADES_UPDATED)

        # Convertir 'AGRAVADO' a boolean
        updated_df['AGRAVADO'] = updated_df['AGRAVADO'].apply(lambda x: True if x == 'X' else False)

        # Normalizar nombres de actividades
        updated_df['ACTIVIDADES'] = updated_df['ACTIVIDADES'].str.strip().apply(lambda x: unidecode(x).lower())
        current_df['ACTIVIDADES'] = current_df['ACTIVIDADES'].str.strip().apply(lambda x: unidecode(x).lower())

        # Identificar nuevas actividades
        new_activities = updated_df[~updated_df['ACTIVIDADES'].isin(current_df['ACTIVIDADES'])]

        for _, row in new_activities.iterrows():
            # Insertar nueva actividad
            insert_activity(row['ACTIVIDADES'], row['AGRAVADO'])
            id_actividad = select_id_activity(row['ACTIVIDADES'])

            if id_actividad:
                # Insertar coberturas para la nueva actividad
                for col in updated_df.columns[1:-1]:  # Excluir 'ACTIVIDADES' y 'AGRAVADO'
                    if row[col] == 'X':
                        id_cobertura = select_id_cobertura(col)
                        if not id_cobertura:
                            insert_cobertura(col)
                            id_cobertura = select_id_cobertura(col)
                        insert_actividad_cobertura(id_actividad, id_cobertura)

        # Verificar y actualizar coberturas de actividades existentes
        existing_activities = updated_df[updated_df['ACTIVIDADES'].isin(current_df['ACTIVIDADES'])]

        for _, row in existing_activities.iterrows():
            id_actividad = select_id_activity(row['ACTIVIDADES'])

            if id_actividad:
                # Insertar coberturas para la actividad existente
                for col in updated_df.columns[1:-1]:  # Excluir 'ACTIVIDADES' y 'AGRAVADO'
                    if row[col] == 'X' and not current_df.loc[current_df['ACTIVIDADES'] == row['ACTIVIDADES'], col].any():
                        id_cobertura = select_id_cobertura(col)
                        if not id_cobertura:
                            insert_cobertura(col)
                            id_cobertura = select_id_cobertura(col)
                        insert_actividad_cobertura(id_actividad, id_cobertura)

        if len(new_activities) == 0: print('No hay datos ha actualizar, la base de datos cuenta con la última versión mas reciente.')
        else: print("Base de datos actualizada correctamente con las nuevas actividades y coberturas.")

    except Exception as e:
        print(f"Error al actualizar la base de datos: {e}")


def load_initial_data():
    try:
        # Leer el archivo fuente
        initial_df = pd.read_excel(paths.DDBB_MANTENIMIENTO_ACTIVIDADES_ACTUAL)
        # Convertir 'AGRAVADO' a boolean
        initial_df['AGRAVADO'] = initial_df['AGRAVADO'].apply(lambda x: True if x == 'X' else False)
        # Normalizar nombres de actividades
        initial_df['ACTIVIDADES'] = initial_df['ACTIVIDADES'].str.strip().apply(lambda x: unidecode(x).lower())

        for _, row in initial_df.iterrows():
            # Insertar nueva actividad
            insert_activity(row['ACTIVIDADES'], row['AGRAVADO'])
            id_actividad = select_id_activity(row['ACTIVIDADES'])
            #print(Connection.execute_select_query("SELECT * FROM catalogo_actividades"))

            if id_actividad:
                # Insertar coberturas para la nueva actividad
                for col in initial_df.columns[1:-1]:  # Excluir 'ACTIVIDADES' y 'AGRAVADO'
                    if row[col] == 'X':
                        id_cobertura = select_id_cobertura(col)
                        if not id_cobertura:
                            insert_cobertura(col)
                            id_cobertura = select_id_cobertura(col)
                        insert_actividad_cobertura(id_actividad, id_cobertura)


        print("Base de datos inicializada correctamente con las actividades y coberturas.")

    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

def execute_options(op=0):
    if op==0: menu()
    elif(op==1): load_initial_data()

def menu():
    menu = 'Seleccione una opción:\n\t1. Descargar actividades y coberturas actuales\n\t2. Actualizar la base de datos con el fichero actualizado\n\t3. Salir\nIntroduzca el número de la opción: '
    op = input(menu)
    while op < '1' or op > '3':
        print('La opcion introducida es incorrecta\n')
        op = input(menu)
    
    if op == '1': 
        print(f"Creando el fichero con las actividades y coberturas actuales.")
        create_all_actividad_cobertura()
        print(f"Archivo guardado en {paths.DDBB_MANTENIMIENTO_ACTIVIDADES_ACTUAL}")
    elif op=='2':
        print(f"Actualizando la base de datos con el fichero actualizado de la ruta {paths.DDBB_MANTENIMIENTO_ACTIVIDADES_UPDATED}") 
        update_database_with_new_data()


if __name__ == '__main__':
    menu()
