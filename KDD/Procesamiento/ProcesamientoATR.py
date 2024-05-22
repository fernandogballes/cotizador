import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import paths

import pandas as pd 
from unidecode import unidecode
import Funciones

def atr_process_all_2014_2022(folder_path):
    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xls') or file.endswith('.xlsx')]
    result_df = pd.DataFrame()
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        df = atr_process_unit_2014_2022(file_path)
        result_df = pd.concat([result_df, df])

    return result_df

def atr_process_unit_2014_2022(excel_path):
    xls = pd.ExcelFile(excel_path)
    # Obtener una lista de los nombres de las hojas excepto las dos primeras
    sheet_names = xls.sheet_names[2:]
    # Crear un diccionario de DataFrames con los sheets seleccionados
    df_all = pd.read_excel(excel_path, sheet_name=sheet_names, engine='openpyxl' if excel_path.endswith('xlsx') else 'xlrd')
   
    process_df = pd.DataFrame()

    for sheet_name, df in df_all.items():

        localidad = unidecode(sheet_name).lower()

        df_filtered = df[(df['Unnamed: 1'] == 'Construcción') | (df['Unnamed: 1'] == 'Construcción de edificios') | (df['Unnamed: 1'] == 'Ingeniería civil') | (df['Unnamed: 1'] == 'Actividades de construcción especializada')]
        df_filtered = df_filtered.iloc[:, 1:11]
        df_filtered = df_filtered.drop(df_filtered.columns[5], axis=1)
        df_filtered = df_filtered.rename(columns={'Unnamed: 1': 'seccion','Unnamed: 2': 'total_jornada', 'Unnamed: 3': 'leves_jornada', 'Unnamed: 4': 'graves_jornada', 'Unnamed: 5': 'mortales_jornada', 'Unnamed: 7': 'total_itinere', 'Unnamed: 8': 'leves_itinere','Unnamed: 9': 'graves_itinere', 'ATR': 'mortales_itinere'})

        df_filtered['comunidad_autonoma'] = localidad
        df_filtered['provincia'] = localidad

        df_filtered = df_filtered.drop_duplicates(subset='seccion')

        process_df = pd.concat([process_df, df_filtered])

    cols_to_replace = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    process_df[cols_to_replace] = process_df[cols_to_replace].infer_objects(copy=False).replace(['-', ' -'], '0')
    process_df[cols_to_replace] = process_df[cols_to_replace].astype(int)
    process_df['seccion'] = process_df['seccion'].apply(lambda x: unidecode(x).lower())

    anio = df['Unnamed: 7'][5]
    process_df['anio'] = int(anio[4:])

    process_df = Funciones.standard_comunidades_provincias(process_df)

    return process_df

def atr_process_all_2001_2002(folder_path):
    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xls')]
    result_df = pd.DataFrame()
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        df = atr_process_unit_2001_2002(file_path)
        result_df = pd.concat([result_df, df])

    return result_df

def atr_process_unit_2001_2002(excel_path):
    xls = pd.ExcelFile(excel_path)
    # Obtener una lista de los nombres de las hojas excepto las dos primeras
    sheet_names = xls.sheet_names[1:]
    # Crear un diccionario de DataFrames con los sheets seleccionados
    df_all = pd.read_excel(excel_path, sheet_name=sheet_names)
    
    process_df = pd.DataFrame()

    for sheet_name, df in df_all.items():

        localidad = unidecode(df.iloc[3,0]).lower().strip()
        anio = str(df.iloc[2,0])
        anio = anio[94:98]

        find_const = df.columns[0]
        df_filtered = df[(df[find_const] == '      CONSTRUCCION...............')]
        
        df_filtered = df_filtered.iloc[:, [0, 5, 6, 7, 8, 9, 10, 11, 12]] 
        df_filtered = df_filtered.rename(columns={find_const: 'seccion','Unnamed: 5': 'total_jornada', 'Unnamed: 6': 'leves_jornada', 'Unnamed: 7': 'graves_jornada', 'Unnamed: 8': 'mortales_jornada', 'Unnamed: 9': 'total_itinere', 'Unnamed: 10': 'leves_itinere','Unnamed: 11': 'graves_itinere', 'Unnamed: 12': 'mortales_itinere'})

        df_filtered['seccion'] = 'construccion'
        df_filtered['comunidad_autonoma'] = localidad
        df_filtered['provincia'] = localidad

        process_df = pd.concat([process_df, df_filtered])

    cols_to_replace = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    process_df[cols_to_replace] = process_df[cols_to_replace].infer_objects(copy=False).replace(['   -      ','   -   ','-'], '0')
    process_df[cols_to_replace] = process_df[cols_to_replace].astype(int)

    process_df['anio'] = int(anio)  

    process_df = Funciones.standard_comunidades_provincias(process_df)
    
    return process_df

def atr_process_all_2003_2013(folders_path): 
    result_df = pd.DataFrame()
    folders = [name for name in os.listdir(folders_path) if os.path.isdir(os.path.join(folders_path, name))]
    for folder in folders:
        path = folders_path + folder
        excel_files = [file for file in os.listdir(path) if file.endswith('.xls') or file.endswith('.xlsx')]

        for file in excel_files:
            file_path = os.path.join(path, file)    
            df = atr_multi_sheets_files_2003_2013(file_path, folder) # MODIFICAR FORMA DE OBTENER EL AÑO
            result_df = pd.concat([result_df, df])

    return result_df

def atr_multi_sheets_files_2003_2013(file, anio):
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names
    df_all = pd.read_excel(file, sheet_name=sheet_names)
   
    process_df = pd.DataFrame()

    for sheet_name, df in df_all.items():

        localidad = unidecode(df.iloc[1,0]).lower()

        if anio < '2009': df_filtered = atr_process_2003_2008(df)
        else: df_filtered = atr_process_2009_2013(df)

        df_filtered['provincia'] = localidad

        process_df = pd.concat([process_df, df_filtered])

    process_df['comunidad_autonoma'] = localidad
    process_df['anio'] = int(anio)
    
    cols_to_replace = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    process_df = process_df.infer_objects(copy=True).replace([' -', '-'], '0')
    process_df[cols_to_replace] = process_df[cols_to_replace].astype(int) 

    process_df = Funciones.standard_comunidades_provincias(process_df)

    return process_df
       
def atr_process_2003_2008(df):
    find_const = df.columns[0]

    df = df[(df[find_const] == 'Construcción.') | (df[find_const] == 'Construcción')]
    df = df.iloc[:, [0, 5, 6, 7, 8, 9, 10, 11, 12]]
    df = df.rename(columns={find_const: 'seccion','Unnamed: 5': 'total_jornada', 'Unnamed: 6': 'leves_jornada', 'Unnamed: 7': 'graves_jornada', 'Unnamed: 8': 'mortales_jornada', 'Unnamed: 9': 'total_itinere', 'Unnamed: 10': 'leves_itinere','Unnamed: 11': 'graves_itinere', 'Unnamed: 12': 'mortales_itinere'})
    
    df['seccion'] = 'construccion'

    return df
    
def atr_process_2009_2013(df):
    df_filtered = df[(df['Unnamed: 1'] == '    Construcción ') | (df['Unnamed: 1'] == 'Construcción de edificios') | (df['Unnamed: 1'] == 'Ingeniería civil') | (df['Unnamed: 1'] == 'Actividades de construcción especializada')]
    df_filtered = df_filtered.iloc[:, 1:11]
    df_filtered = df_filtered.drop(df_filtered.columns[5], axis=1)
    df_filtered = df_filtered.rename(columns={'Unnamed: 1': 'seccion','Unnamed: 2': 'total_jornada', 'Unnamed: 3': 'leves_jornada', 'Unnamed: 4': 'graves_jornada', 'Unnamed: 5': 'mortales_jornada',  'Unnamed: 7': 'total_itinere', 'Unnamed: 8': 'leves_itinere','Unnamed: 9': 'graves_itinere', 'Unnamed: 10': 'mortales_itinere'})

    #df_filtered['seccion'] = df_filtered['seccion'].str.strip()
    df_filtered['seccion'] = df_filtered['seccion'].str.strip().apply(lambda x: unidecode(x).lower())
    
    return df_filtered

def create_atr_2001_2022():
    atr_2001_2002 = atr_process_all_2001_2002(paths.RAW_ATR_2001_2002_PATH)
    atr_2003_2013 = atr_process_all_2003_2013(paths.RAW_ATR_2003_2013_PATH)
    atr_2014_2022 = atr_process_all_2014_2022(paths.RAW_ATR_2014_2022_PATH)
    
    atr_2001_2022 = pd.concat([atr_2001_2002,atr_2003_2013,atr_2014_2022])

    num_columns = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    atr_2001_2022[num_columns] = atr_2001_2022[num_columns].astype(float)/1000

    Funciones.create_excel(atr_2001_2022, paths.SILVER_ATR_2001_2022_PATH) 

if __name__ == '__main__':
    create_atr_2001_2022()





    
