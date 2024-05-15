import csv
import os
import pandas as pd 
from unidecode import unidecode
import json
import unicodedata
import Funciones

def poblacion_activa_ocupada_process(df):

    # Estandarizamos los nombres de las columnas
    df.columns = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8').lower() for col in df.columns]
    df.rename(columns={'provincias': 'provincia'}, inplace=True)

    df = df.dropna(subset=['provincia']).copy() # Eliminamos todas las filas que no tengan valor en la columna porvincia, ya que estas son totales nacionales que no queremos
    df['provincia'] = df['provincia'].apply(lambda x: unidecode(x).lower()).astype(str) # Eliminamos acentos y caracteres especiales
    df[['codigo_provincia', 'provincia']] = df['provincia'].str.extract(r'(\d+) (.+)') # Extraemos el codigo de provincia y el nombre de la provincia

    df = Funciones.standard_comunidades_provincias(df) 

    df[['anio', 'trimestre']] = df['periodo'].str.extract(r'(\d{4})T(\d)') # Extraemos el año y el trimestre
    df = df.drop('periodo', axis=1)

    df[['anio', 'codigo_provincia', 'trimestre']] = df[['anio', 'codigo_provincia', 'trimestre']].astype(int)

    df['total'] = df['total'].infer_objects(copy=False).replace(r'^..$', '0', regex=True) # Cambiamos valores nulos por 0
    
    # Modificamos la cadena para que sea compatible con el formato float
    df['total'] = df['total'].str.replace('.', '')
    df['total'] = df['total'].str.replace(',', '.')
    df['total'] = df['total'].astype(float)
    
    return df

def poblacion_activa_process(folder_path):
    df = pd.read_csv(folder_path, sep=';', encoding='utf-8')
    df = df.drop('Total Nacional', axis=1) # Eliminamos columna de total nacional, siempre es igual, no aporta informacion
    
    df = poblacion_activa_ocupada_process(df)

    edad_mapping = {'Total': '1','De 16 a 19 años': '2', 'De 20 a 24 años': '3', 'De 25 a 54 años': '4', '55 y más años': '5'}
    df['edad'] = df['edad'].astype(str).replace(edad_mapping).astype(int)

    df = df.reindex(columns=['anio', 'trimestre', 'codigo_provincia', 'provincia', 'comunidad_autonoma', 'edad', 'total'])
    
    return df

def poblacion_ocupada_process(folder_path):
    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    result_df = pd.DataFrame()
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')

        df = df[(df['Sector económico']=='Construcción')]
        df = df[df['Provincias'] != 'Total Nacional']

        df = poblacion_activa_ocupada_process(df)
        result_df = pd.concat([result_df, df])

    result_df = result_df.reindex(columns=['anio', 'trimestre', 'codigo_provincia', 'provincia', 'comunidad_autonoma', 'total'])
    result_df.sort_values(by=['anio', 'codigo_provincia'], inplace=True)

    return result_df

def create_poblacion_activa_2002_2023():
    df_activa = poblacion_activa_process('datos/poblacion activa y ocupada/poblacion activa/65351.csv')
    Funciones.create_excel(df_activa, 'results/SILVER/', 'poblacion_activa_2002_2023.xlsx')
    
def create_poblacion_ocupada_2002_2023():
    df_ocupada = poblacion_ocupada_process('datos/poblacion activa y ocupada/poblacion ocupada/')
    Funciones.create_excel(df_ocupada, 'results/SILVER/', 'poblacion_ocupada_2002_2023.xlsx')

def create_poblacion_ocupada_activa_2002_2023():
    create_poblacion_activa_2002_2023()
    create_poblacion_ocupada_2002_2023()

if __name__ == '__main__':
    create_poblacion_ocupada_activa_2002_2023()