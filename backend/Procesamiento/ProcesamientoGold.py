import csv
import os
import pandas as pd 
from unidecode import unidecode
import json
import unicodedata
import Funciones

def procces_gold_poblacion_activa_ocupada():
    df_activa = pd.read_excel('results/SILVER/poblacion_activa_2002_2023.xlsx')
    df_ocupada = pd.read_excel('results/SILVER/poblacion_ocupada_2002_2023.xlsx')

    df_activa = df_activa.rename(columns={'total': 'total_poblacion_activa'})
    df_ocupada = df_ocupada.rename(columns={'total': 'total_poblacion_ocupada'})

    df_ocupada['edad'] = 1
    
    merged_df = df_activa.merge(df_ocupada, on=['comunidad_autonoma', 'anio', 'trimestre', 'codigo_provincia', 'edad', 'provincia'])
    merged_df = merged_df.drop('edad', axis = 1)
    merged_df = merged_df[merged_df['anio'] <= 2022]

    df_mean = merged_df.groupby(['anio', 'provincia', 'comunidad_autonoma']).agg({'total_poblacion_activa': 'mean', 'total_poblacion_ocupada': 'mean'}).reset_index()

    df_comunidades = df_mean.groupby(['comunidad_autonoma', 'anio']).agg({'total_poblacion_activa': 'sum', 'total_poblacion_ocupada': 'sum'}).reset_index()
    df_comunidades['provincia'] = df_comunidades['comunidad_autonoma']

    df_result = pd.concat([df_mean, df_comunidades])
    df_result = df_result.drop_duplicates()

    df_result['porcentaje_poblacion_ocupada'] = df_result['total_poblacion_ocupada']/df_result['total_poblacion_activa']

    return df_result

def process_gold_atr():
    df = pd.read_excel('results/SILVER/ATR_2001_2022.xlsx')
    df = df[(df['seccion']=='construccion') & (df['anio']>2001)]
    df = df[['total_jornada', 'total_itinere', 'comunidad_autonoma', 'provincia', 'anio']]
    df = df.rename(columns={'total_jornada': 'total_accidentes_jornada', 'total_itinere': 'total_accidentes_itinere'})

    return df

def process_gold_accidentes_trafico():
    df = pd.read_excel('results/SILVER/accidentes_trafico_2002_2022.xlsx')

    df = df[df['tipo']=='total victimas']
    df = df.drop('tipo', axis = 1)
    df = df.rename(columns={'numero': 'total_victimas_trafico'})

    return df
    
def create_gold():
    df_poblacion_activa_ocupada = procces_gold_poblacion_activa_ocupada()
    df_atr = process_gold_atr()
    df_accidentes_trafico = process_gold_accidentes_trafico()

    df_merged_1 = df_poblacion_activa_ocupada.merge(df_atr, on=['anio', 'provincia', 'comunidad_autonoma'])
    df_merged_2 = df_merged_1.merge(df_accidentes_trafico, on=['anio', 'provincia', 'comunidad_autonoma'])

    df_merged_2.sort_values(by=['anio', 'comunidad_autonoma'], inplace=True)
    
    Funciones.create_excel(df_merged_2, 'results/GOLD/', 'gold.xlsx')

def create_gold_poblacion_activa_ocupada():
    df = procces_gold_poblacion_activa_ocupada()
    Funciones.create_excel(df, 'results/GOLD/', 'poblacion_activa_ocupada.xlsx')

if __name__ == '__main__':
    create_gold()
