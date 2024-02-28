import csv
import os
import pandas as pd 
from unidecode import unidecode
import json
import unicodedata

comunidades_autonomas = ['madrid (comunidad de) ', 'navarra (c. foral de)','murcia (region de)','balears (illes)', 'balears', 'asturias (principado de)', 'andalucia', 'aragon', 'asturias', 'baleares', 'canarias', 'cantabria', 'castilla-la mancha', 'castilla y leon', 'cataluna', 'comunitat valenciana', 'comunidad valenciana', 'extremadura', 'galicia', 'madrid', 'murcia', 'navarra', 'pais vasco', 'rioja (la)', 'ceuta', 'melilla', 'la rioja']
comunidades_dict = {'balears': 'baleares', 'coruna (a)': 'a coruna', 'castilla-la mancha': 'castilla la mancha', 'madrid (comunidad de) ': 'madrid', 'navarra (c. foral de)': 'navarra', 'murcia (region de)': 'murcia', 'balears (illes)': 'baleares', 'asturias (principado de)': 'asturias', 'comunitat valenciana': 'comunidad valenciana', 'rioja (la)': 'la rioja'}

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

        if localidad in comunidades_autonomas: comunidad_autonoma = localidad

        df_filtered = df[(df['Unnamed: 1'] == 'Construcción') | (df['Unnamed: 1'] == 'Construcción de edificios') | (df['Unnamed: 1'] == 'Ingeniería civil') | (df['Unnamed: 1'] == 'Actividades de construcción especializada')]
        df_filtered = df_filtered.iloc[:, 1:11]
        df_filtered = df_filtered.drop(df_filtered.columns[5], axis=1)
        df_filtered = df_filtered.rename(columns={'Unnamed: 1': 'seccion','Unnamed: 2': 'total_jornada', 'Unnamed: 3': 'leves_jornada', 'Unnamed: 4': 'graves_jornada', 'Unnamed: 5': 'mortales_jornada', 'Unnamed: 7': 'total_itinere', 'Unnamed: 8': 'leves_itinere','Unnamed: 9': 'graves_itinere', 'ATR': 'mortales_itinere'})


        df_filtered['comunidad_autonoma'] = comunidad_autonoma
        df_filtered['provincia'] = localidad

        df_filtered = df_filtered.drop_duplicates(subset='seccion')

        process_df = pd.concat([process_df, df_filtered])

    cols_to_replace = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    process_df[cols_to_replace] = process_df[cols_to_replace].infer_objects(copy=False).replace(['-', ' -'], '0')
    process_df[cols_to_replace] = process_df[cols_to_replace].astype(int)
    process_df['seccion'] = process_df['seccion'].apply(lambda x: unidecode(x).lower())


    #process_df['anio'] = int(excel_path[31:35])
    anio = df['Unnamed: 7'][5]
    process_df['anio'] = int(anio[4:])

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

        comunidad_autonoma = unidecode(df.iloc[3,0]).lower().strip()
        anio = str(df.iloc[2,0])
        anio = anio[94:98]

        find_const = df.columns[0]
        df_filtered = df[(df[find_const] == '      CONSTRUCCION...............')]
        
        df_filtered = df_filtered.iloc[:, [0, 5, 6, 7, 8, 9, 10, 11, 12]] 
        df_filtered = df_filtered.rename(columns={find_const: 'seccion','Unnamed: 5': 'total_jornada', 'Unnamed: 6': 'leves_jornada', 'Unnamed: 7': 'graves_jornada', 'Unnamed: 8': 'mortales_jornada', 'Unnamed: 9': 'total_itinere', 'Unnamed: 10': 'leves_itinere','Unnamed: 11': 'graves_itinere', 'Unnamed: 12': 'mortales_itinere'})

        df_filtered['seccion'] = 'construccion'
        df_filtered['comunidad_autonoma'] = comunidad_autonoma
        df_filtered['provincia'] = comunidad_autonoma


        process_df = pd.concat([process_df, df_filtered])

    cols_to_replace = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    process_df[cols_to_replace] = process_df[cols_to_replace].infer_objects(copy=False).replace(['   -      ','   -   ','-'], '0')
    process_df[cols_to_replace] = process_df[cols_to_replace].astype(int)

    process_df['anio'] = int(anio)    
    
    return process_df

def atr_process_all_2003_2013(folders_path): 
    result_df = pd.DataFrame()
    folders = [name for name in os.listdir(folders_path) if os.path.isdir(os.path.join(folders_path, name))]
    for folder in folders:
        path = folders_path + folder
        excel_files = [file for file in os.listdir(path) if file.endswith('.xls') or file.endswith('.xlsx')]

        for file in excel_files:
            file_path = os.path.join(path, file)    
            df = atr_multi_sheets_files_2003_2013(file_path, folder)
            result_df = pd.concat([result_df, df])

    return result_df
    
def atr_multi_sheets_files_2003_2013(file, anio):
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names
    df_all = pd.read_excel(file, sheet_name=sheet_names)
   
    process_df = pd.DataFrame()

    for sheet_name, df in df_all.items():

        provincia = unidecode(df.iloc[1,0]).lower()
        #print(anio, provincia, file)

        if provincia in comunidades_autonomas: comunidad_autonoma = provincia

        if anio < '2009': df_filtered = atr_process_2003_2008(df)
        else: df_filtered = atr_process_2009_2013(df)

        df_filtered['provincia'] = provincia

        process_df = pd.concat([process_df, df_filtered])

    process_df['comunidad_autonoma'] = comunidad_autonoma
    process_df['anio'] = int(anio)
    
    cols_to_replace = ['total_jornada', 'leves_jornada', 'graves_jornada', 'mortales_jornada', 'total_itinere', 'leves_itinere', 'graves_itinere', 'mortales_itinere']
    process_df = process_df.infer_objects(copy=True).replace([' -', '-'], '0')
    process_df[cols_to_replace] = process_df[cols_to_replace].astype(int) 

    return process_df
       
def atr_process_2003_2008(df):
    find_const = df.columns[0]
    comunidad_autonoma = unidecode(df.iloc[1,0]).lower()

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

def poblacion_activa_ocupada_process(df):

    df.columns = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8').lower() for col in df.columns]
    df.rename(columns={'provincias': 'provincia'}, inplace=True)

    with open('backend/diccionario_comunidades.json', 'r') as file: comunidades_dict = json.load(file)

    df = df.dropna(subset=['provincia']).copy()
    df['provincia'] = df['provincia'].apply(lambda x: unidecode(x).lower()).astype(str)
    df[['codigo_provincia', 'provincia']] = df['provincia'].str.extract(r'(\d+) (.+)')

    # Definir una función lambda para buscar el mapeo basado en el contenido
    comunidades_mapping = lambda x: next((v for k, v in comunidades_dict.items() if k in x.lower()), x)
    provincias_mapping = {'balears, illes': 'baleares', 'bizkaia': 'vizcaya', 'coruna, a': 'a coruna', 'gipuzkoa': 'guipuzcoa', 'palmas': 'las palmas', 'rioja, la': 'la rioja', 'alicante/alacant': 'alicante', 'araba/alava': 'alava', 'castellon/castello': 'castellon', 'valencia/valencia': 'valencia'}

    df['provincia'] = df['provincia'].infer_objects(copy=False).replace(provincias_mapping)
    df['comunidad_autonoma'] = df['provincia'].map(comunidades_mapping)

    df[['anio', 'trimestre']] = df['periodo'].str.extract(r'(\d{4})T(\d)')
    df = df.drop('periodo', axis=1)

    df[['anio', 'codigo_provincia', 'trimestre']] = df[['anio', 'codigo_provincia', 'trimestre']].astype(int)

    df['total'] = df['total'].infer_objects(copy=False).replace(r'^..$', '0', regex=True)
    df['total'] = df['total'].infer_objects(copy=False).replace(['\.', '\,'], '', regex=True).astype(float)/10

    #print(df[~df['total'].str.contains('^\d+$')])
    
    return df

def poblacion_activa_process(folder_path):
    df = pd.read_csv(folder_path, sep=';', encoding='latin1')
    df = df.drop('Total Nacional', axis=1)
    
    df = poblacion_activa_ocupada_process(df)

    edad_mapping = {'Total': '1','De 16 a 19 años': '2', 'De 20 a 24 años': '3', 'De 25 a 54 años': '4', '55 y más años': '5'}
    df['edad'] = df['edad'].astype(str).replace(edad_mapping).astype(int)

    df = df.reindex(columns=['anio', 'trimestre', 'codigo_provincia', 'provincia', 'comunidad_autonoma', 'edad', 'total'])
    
    return df

def poblacion_ocupada_process(folder_path):
    df = pd.read_csv(folder_path, sep=';', encoding='latin1')
    df = df[(df['Sector económico']=='Construcción')]
    df = df[df['Provincias'] != 'Total Nacional']

    df = poblacion_activa_ocupada_process(df)

    df = df.reindex(columns=['anio', 'trimestre', 'codigo_provincia', 'provincia', 'comunidad_autonoma', 'total'])

    return df

def create_silver_data():
    create_atr_2001_2022()
    create_poblacion_activa_2002_2023()
    create_poblacion_ocupada_2002_2023()

def create_atr_2001_2022():
    atr_2001_2002 = atr_process_all_2001_2002('datos/accidentes/2001-2002/')
    atr_2003_2013 = atr_process_all_2003_2013('datos/accidentes/2003-2013/')
    atr_2014_2022 = atr_process_all_2014_2022('datos/accidentes/2014-2022/')
    
    atr_2001_2022 = pd.concat([atr_2001_2002,atr_2003_2013,atr_2014_2022])
    
    columns_replace = ['provincia', 'comunidad_autonoma']
    atr_2001_2022[columns_replace] = atr_2001_2022[columns_replace].replace(comunidades_dict)

    create_excel(atr_2001_2022, 'results/', 'ATR_2001_2022.xlsx')

def create_poblacion_activa_2002_2023():
    df_activa = poblacion_activa_process('datos/ocupacion/activos_por_grupo_de_edad_y_provincia.csv')
    create_excel(df_activa, 'results/', 'poblacion_activa_2002_2023.xlsx')
    
def create_poblacion_ocupada_2002_2023():
    df_ocupada = poblacion_ocupada_process('datos/ocupacion/ocupados_por_sector_economico_y_provincia.csv')
    create_excel(df_ocupada, 'results/', 'poblacion_ocupada_2002_2023.xlsx')

def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

if __name__ == '__main__':

    #atr_2014_2022 = atr_process_all_2014_2022('datos/accidentes/2014-2022/')
    create_silver_data()
    #df_ocupada = poblacion_ocupada_process('ocupacion/ocupados_por_sector_economico_y_provincia.csv')
    #df_activa = poblacion_activa_process('datos/ocupacion/activos_por_grupo_de_edad_y_provincia.csv')
    #print(df_activa)
    """ df_activa = poblacion_activa_process('datos/ocupacion/activos_por_grupo_de_edad_y_provincia.csv')
    print(df_activa)
    print(df_activa['provincia'].unique())
    print(df_activa['codigo_provincia'].unique()) """



    
