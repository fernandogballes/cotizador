import csv
import os
import pandas as pd 
from unidecode import unidecode
import json
import unicodedata
import Funciones

def accidentes_trafico_procces(folder_path):
    df = pd.read_csv(folder_path, sep=',', dtype=str)

    df = df.drop('numero1', axis=1).copy()
    df = df.rename(columns={'comunidad': 'comunidad_autonoma','Tipo': 'tipo', 'year': 'anio', 'Textbox6': 'comunidad_subtotal', 'Textbox7': 'numero_subtotal'})

    columns = ['comunidad_autonoma','provincia','comunidad_subtotal', 'tipo']
    df[columns] = df[columns].apply(lambda x: x.apply(lambda y: unidecode(y).lower()))
    df[['numero', 'numero_subtotal']] = df[['numero', 'numero_subtotal']].infer_objects(copy=False).replace(['\.', '\,'], '', regex=True).astype(float)
    df['anio'] = df['anio'].astype(int)
    df['comunidad_subtotal'] = df['comunidad_subtotal'].str.slice(9)

    df_comunidades = df[['comunidad_subtotal', 'numero_subtotal','tipo', 'anio']]
    df_provincias = df[['comunidad_autonoma', 'provincia', 'anio', 'tipo', 'numero']]

    df_comunidades = df_comunidades.drop_duplicates()
    df_comunidades = df_comunidades.rename(columns={'numero_subtotal': 'numero', 'comunidad_subtotal': 'comunidad_autonoma'})
    df_comunidades['provincia'] = df_comunidades['comunidad_autonoma']

    df_total = pd.concat([df_provincias, df_comunidades])

    df_total.sort_values(by=['comunidad_autonoma', 'anio'], inplace=True)
    df_total = Funciones.standard_comunidades_provincias(df_total)

    df_total = df_total.drop_duplicates()
    df_total ['numero'] = df_total['numero'].astype(float)/1000

    return df_total

def create_accidentes_trafico():
    df = accidentes_trafico_procces('datos/accidentes trafico/Accidentes_victimas_Carr__CCAA_provincia (1).csv')
    Funciones.create_excel(df, 'results/SILVER/', 'accidentes_trafico_2002_2022.xlsx')

if __name__ == '__main__':
    create_accidentes_trafico()