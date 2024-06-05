import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import paths

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib
import json
from sklearn.metrics import classification_report, confusion_matrix

def prepare_data(data,option=0):
    # Identificar las columnas categóricas y numéricas
    categorical_cols = ['provincia', 'comunidad_autonoma']
    numeric_cols = ['anio']

    # Transformación de columnas categóricas y numéricas
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(), categorical_cols)
        ])
    
    # Aplicar la transformación
    X = preprocessor.fit_transform(data.drop('cluster', axis=1))
    y = data['cluster']
    
    return X, y, preprocessor

def predict_random_forest(work_data):
    X, y, preprocessor = prepare_data(work_data)

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Entrenar el modelo de Random Forest
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    # Realizar predicciones
    y_pred = rf_classifier.predict(X_test)

    # Evaluar el rendimiento del modelo
    print('CONFUSION MATRIX')
    print(confusion_matrix(y_test, y_pred))
    print('\nREPORT')
    print(classification_report(y_test, y_pred))

    # Guardar el modelo y el preprocesador para futuras predicciones
    #if option == 1:
    if input('0. No guardar modelo\n1. Guardar modelo\nSeleccione: ') == '1':
        joblib.dump(rf_classifier, paths.TRAINED_PREDICTION_MODEL_PATH)
        joblib.dump(preprocessor, paths.PREPROCESSOR_PATH)

def test():
    # Nuevos datos para predicción (por ejemplo, datos del año 2025)
    with open(paths.SEMAFORO_DICT_PATH, 'r') as file: semaforizacion_dict = json.load(file)
    rf_classifier = joblib.load(paths.TRAINED_PREDICTION_MODEL_PATH)
    preprocessor = joblib.load(paths.PREPROCESSOR_PATH)
    new_data = pd.DataFrame({
        'anio': [2025],
        'provincia': ['malaga'],
        'comunidad_autonoma': ['andalucia']
    })

    # Preprocesar los nuevos datos
    X_new = preprocessor.transform(new_data)

    # Realizar predicción
    new_cluster_prediction = rf_classifier.predict(X_new)
    predicted_cluster = new_cluster_prediction[0]

    # Obtener el semáforo correspondiente al cluster predicho
    predicted_semaforo = semaforizacion_dict[str(predicted_cluster)]

    print(new_data)
    print(f'El cluster predicho para los nuevos datos es: {predicted_cluster}')
    print(f'El semáforo correspondiente al cluster predicho es: {predicted_semaforo}')

def run_selector(op=0):
    data = pd.read_excel(paths.CLUSTERED_DATA_PATH)  # Carga tu conjunto de datos
    work_data = data[['anio', 'provincia', 'comunidad_autonoma', 'cluster']]
    
    if op == 0: test()
    elif op == 1: predict_random_forest(work_data)


if __name__ == '__main__':
    run_selector(op=0)