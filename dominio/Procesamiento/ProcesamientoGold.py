import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import config

import pandas as pd 
from unidecode import unidecode
import Funciones

def procces_gold_poblacion_activa_ocupada():
    df_activa = pd.read_excel(config.SILVER_POBLACION_ACTIVA_PATH)
    df_ocupada = pd.read_excel(config.SILVER_POBLACION_OCUPADA_PATH)

    df_activa = df_activa.rename(columns={'total': 'total_poblacion_activa'})
    df_ocupada = df_ocupada.rename(columns={'total': 'total_poblacion_ocupada_construccion'})

    # Creamos una columna edad con valor a 1 ya que en la pobacion activa este grupo representa el total, con el cual queremos comparar
    # df_ocupada['edad'] = 1
    df_activa = df_activa[df_activa['edad']==1]
    df_activa = df_activa.drop('edad', axis = 1)
    
    merged_df = df_activa.merge(df_ocupada, on=['comunidad_autonoma', 'anio', 'trimestre', 'codigo_provincia', 'provincia'])
    merged_df = merged_df[(merged_df['anio'] <= 2022) & (merged_df['anio'] >= 2003)]

    # Creacion de medias anuales y que los datos vienen en trimestres
    df_mean = merged_df.groupby(['anio', 'provincia', 'comunidad_autonoma']).agg({'total_poblacion_activa': 'mean', 'total_poblacion_ocupada_construccion': 'mean'}).reset_index()
    
    df_result = df_mean
    df_result = df_result.drop_duplicates()

    return df_result

def process_gold_atr():
    df = pd.read_excel(config.SILVER_ATR_2001_2022_PATH)
    df = df[(df['seccion']=='construccion') & (df['anio']>2002)]
    df = df.rename(columns={'total_jornada': 'total_accidentes_jornada', 'total_itinere': 'total_accidentes_itinere', 'leves_jornada': 'leves_accidentes_jornada', 'graves_jornada': 'graves_accidentes_jornada', 'mortales_jornada': 'mortales_accidentes_jornada', 'leves_itinere': 'leves_accidentes_itinere', 'graves_itinere': 'graves_accidentes_itinere', 'mortales_itinere': 'mortales_accidentes_itinere'})

    return df

def process_gold_accidentes_trafico():
    df = pd.read_excel(config.SILVER_ACCIDENTES_TRAFICO_PATH)

    df = df[df['tipo']=='total victimas']
    df = df.drop('tipo', axis = 1)
    df = df.rename(columns={'numero': 'total_victimas_trafico'})

    return df

def multiply_columns(df):
    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    columnas_numericas = columnas_numericas.drop(['anio'])
    df[columnas_numericas] *= 1000

    return df

def create_ratios(df):
    df_copy = df.copy()
    df_copy = multiply_columns(df_copy)

    df_copy['accidentes_leves_jornada_por_persona'] = df_copy['leves_accidentes_jornada']/df_copy['total_poblacion_ocupada_construccion']
    df_copy['accidentes_graves_jornada_por_persona'] = df_copy['graves_accidentes_jornada']/df_copy['total_poblacion_ocupada_construccion']
    df_copy['accidentes_mortales_jornada_por_persona'] = df_copy['mortales_accidentes_jornada']/df_copy['total_poblacion_ocupada_construccion']

    df_copy['accidentes_leves_itinere_por_persona'] = df_copy['leves_accidentes_itinere']/df_copy['total_poblacion_ocupada_construccion']
    df_copy['accidentes_graves_itinere_por_persona'] = df_copy['graves_accidentes_itinere']/df_copy['total_poblacion_ocupada_construccion']
    df_copy['accidentes_mortales_itinere_por_persona'] = df_copy['mortales_accidentes_itinere']/df_copy['total_poblacion_ocupada_construccion']

    df_copy['accidentes_trafico_por_persona'] = (df_copy['total_victimas_trafico'] * (df_copy['total_poblacion_ocupada_construccion']/df_copy['total_poblacion_activa'])) /df_copy['total_poblacion_ocupada_construccion']

    df_copy = df_copy[['anio', 'provincia', 'comunidad_autonoma', 'accidentes_leves_jornada_por_persona', 'accidentes_graves_jornada_por_persona', 'accidentes_mortales_jornada_por_persona','accidentes_leves_itinere_por_persona','accidentes_graves_itinere_por_persona','accidentes_mortales_itinere_por_persona','accidentes_trafico_por_persona']]

    return df_copy

def create_gold():
    df_poblacion_activa_ocupada = procces_gold_poblacion_activa_ocupada()
    df_atr = process_gold_atr()
    df_accidentes_trafico = process_gold_accidentes_trafico()

    df_merged_1 = df_poblacion_activa_ocupada.merge(df_atr, on=['anio', 'provincia', 'comunidad_autonoma'])
    df_merged_2 = df_merged_1.merge(df_accidentes_trafico, on=['anio', 'provincia', 'comunidad_autonoma'])

    df_merged_2.sort_values(by=['anio', 'comunidad_autonoma'], inplace=True)

    df_merged_2 =df_merged_2.drop(columns='seccion')

    df_gold = create_ratios(df_merged_2)
    
    Funciones.create_excel(df_gold, config.GOLD_DATA_PATH)

if __name__ == '__main__':
    create_gold()
