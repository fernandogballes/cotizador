import os
import pandas as pd 
import json

def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

def standard_comunidades_provincias(df):
    with open('backend/diccionario_comunidades_provincias.json', 'r') as file: comunidades_dict = json.load(file)
    with open('backend/diccionario_estandar_comunidades.json', 'r') as file: estandar_dict = json.load(file)

    df['provincia'] = df['provincia'].infer_objects(copy=False).replace(estandar_dict)
    df['comunidad_autonoma'] = df['provincia'].infer_objects(copy=False).replace(comunidades_dict)

    return df