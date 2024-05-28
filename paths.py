import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/') + '/'

# MODELS PATHS
TRAINED_DISTANCE_MATRIX_MODEL_PATH = BASE_DIR + 'KDD/Algoritmos/trained_models/random_forest_distance_matrix.joblib'
TRAINED_PREDICTION_MODEL_PATH = BASE_DIR + 'KDD/Algoritmos/trained_models/random_forest_cluster_predictor.joblib'
CLUSTERED_DATA_PATH = BASE_DIR + 'KDD/Algoritmos/cluster_data/cluster_data.xlsx'
PREPROCESSOR_PATH = BASE_DIR + 'KDD/Algoritmos/trained_models/preprocessor.joblib'


# DATA PATHS
# RAW DATA
RAW_ATR_2001_2002_PATH = BASE_DIR + 'KDD/data/RAW/accidentes laborales/2001-2002/'
RAW_ATR_2003_2013_PATH = BASE_DIR + 'KDD/data/RAW/accidentes laborales/2003-2013/'
RAW_ATR_2014_2022_PATH = BASE_DIR + 'KDD/data/RAW/accidentes laborales/2014-2022/'

RAW_POBLACION_ACTIVA_PATH = BASE_DIR + 'KDD/data/RAW/poblacion activa y ocupada/poblacion activa/65351.csv'
RAW_POBLACION_OCUPADA_PATH = BASE_DIR + 'KDD/data/RAW/poblacion activa y ocupada/poblacion ocupada/'

RAW_ACCIDENTES_TRAFICO_PATH = BASE_DIR + 'KDD/data/RAW/accidentes trafico/Accidentes_victimas_Carr__CCAA_provincia.csv'
# SILVER DATA
SILVER_ATR_2001_2022_PATH = BASE_DIR + 'KDD/data/SILVER/ATR_2001_2022.xlsx'
SILVER_POBLACION_OCUPADA_PATH = BASE_DIR + 'KDD/data/SILVER/poblacion_ocupada_2002_2023.xlsx'
SILVER_POBLACION_ACTIVA_PATH = BASE_DIR + 'KDD/data/SILVER/poblacion_activa_2002_2023.xlsx'
SILVER_ACCIDENTES_TRAFICO_PATH =  BASE_DIR + 'KDD/data/SILVER/accidentes_trafico_2002_2022.xlsx'
# GOLD DATA
GOLD_DATA_PATH = BASE_DIR + 'KDD/data/GOLD/gold.xlsx'


# DICTIONARY PATHS
SEMAFORO_DICT_PATH = BASE_DIR + 'KDD/Algoritmos/cluster_data/semaforo_dict.json'
COMUNIDADES_PROVINCIAS_DICT_PATH = BASE_DIR + 'KDD/Procesamiento/diccionario_comunidades_provincias.json'
STANDARD_COMUNIDADES_DICT_PATH = BASE_DIR + 'KDD/Procesamiento/diccionario_estandar_comunidades.json'

# BBDD PATHS
DDBB_PATH = BASE_DIR + 'Sistema/bbdd/data/'
DDBB_CONFIG_PATH = BASE_DIR + 'Sistema/bbdd/config/ddbb_config.txt'
DDBB_TRIGGER_PATH = BASE_DIR + 'Sistema/bbdd/tool_querys/trigger.sql'
DDBB_MANTENIMIENTO_ACTIVIDADES_ACTUAL = DDBB_PATH + 'Mantenimiento actividades/actividades_coberturas_actual.xlsx'
DDBB_MANTENIMIENTO_ACTIVIDADES_UPDATED = DDBB_PATH + 'Mantenimiento actividades/actividades_coberturas_updated.xlsx'
BBDD_DELETE_QUERYS = BASE_DIR + 'Sistema/bbdd/tool_querys/delete_drop.sql'