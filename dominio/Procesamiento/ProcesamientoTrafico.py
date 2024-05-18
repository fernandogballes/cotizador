import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import config

import pandas as pd 
from unidecode import unidecode
import Funciones

def accidentes_trafico_procces(folder_path):
    df = pd.read_csv(folder_path, sep=',', dtype=str)

    df = df.drop('numero1', axis=1).copy()
    df = df.rename(columns={'comunidad': 'comunidad_autonoma','Tipo': 'tipo', 'year': 'anio', 'Textbox6': 'comunidad_subtotal', 'Textbox7': 'numero_subtotal'})

    columns = ['comunidad_autonoma','provincia','comunidad_subtotal', 'tipo']
    df[columns] = df[columns].apply(lambda x: x.apply(lambda y: unidecode(y).lower()))
    #df[['numero', 'numero_subtotal']] = df[['numero', 'numero_subtotal']].infer_objects(copy=False).replace(['\.', '\,'], '', regex=True).astype(float) # REVISAR NUMEROS
    df['numero'] = df['numero'].str.replace('.', '').astype(float)
    df['numero_subtotal'] = df['numero_subtotal'].str.replace('.', '').astype(float)

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
    df = accidentes_trafico_procces(config.RAW_ACCIDENTES_TRAFICO_PATH)
    Funciones.create_excel(df, config.SILVER_ACCIDENTES_TRAFICO_PATH)

if __name__ == '__main__':
    create_accidentes_trafico()