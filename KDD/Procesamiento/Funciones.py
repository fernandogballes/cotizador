import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import paths

import pandas as pd 
import json

def create_excel(df, full_path):
    output_folder = os.path.dirname(full_path)
    file_name = os.path.basename(full_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df.to_excel(full_path, index=False)

def standard_comunidades_provincias(df):
    with open(paths.COMUNIDADES_PROVINCIAS_DICT_PATH, 'r') as file: comunidades_dict = json.load(file)
    with open(paths.STANDARD_COMUNIDADES_DICT_PATH, 'r') as file: estandar_dict = json.load(file)

    df['provincia'] = df['provincia'].infer_objects(copy=False).replace(estandar_dict)
    df['comunidad_autonoma'] = df['provincia'].infer_objects(copy=False).replace(comunidades_dict)

    provincias = comunidades_dict.keys()
    df = df[df['provincia'].isin(provincias)]

    return df