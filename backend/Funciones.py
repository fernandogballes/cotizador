import csv
import os
import pandas as pd 
from unidecode import unidecode
import json
import unicodedata

def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

def standarized_comunidades_provincias(localidad):
    with open('backend/diccionario_comunidades_provincias.json', 'r') as file: comunidades_dict = json.load(file)
    with open('backend/diccionario_estandar_comunidades.json', 'r') as file: estandar_dict = json.load(file)

    if estandar_dict.get(localidad) != None: localidad = estandar_dict.get(localidad)
    comunidad_autonoma = comunidades_dict.get(localidad, localidad)

    return localidad, comunidad_autonoma

def standard(df):
    with open('backend/diccionario_comunidades_provincias.json', 'r') as file: comunidades_dict = json.load(file)
    with open('backend/diccionario_estandar_comunidades.json', 'r') as file: estandar_dict = json.load(file)

    df['provincia'] = df['provincia'].infer_objects(copy=False).replace(estandar_dict)
    df['comunidad_autonoma'] = df['provincia'].infer_objects(copy=False).replace(comunidades_dict)

    return df