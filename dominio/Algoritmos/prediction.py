import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import squareform 
import os
import joblib
import json
from sklearn.metrics import classification_report, confusion_matrix

def prepare_data(data):
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

def predict_random_forest(data):
    X, y, preprocessor = prepare_data(work_data)

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Entrenar el modelo de Random Forest
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    # Realizar predicciones
    y_pred = rf_classifier.predict(X_test)

    # Evaluar el rendimiento del modelo
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Guardar el modelo y el preprocesador para futuras predicciones
    joblib.dump(rf_classifier, 'random_forest_cluster_predictor.joblib')
    joblib.dump(preprocessor, 'preprocessor.joblib')

def test():
    # Nuevos datos para predicción (por ejemplo, datos del año 2025)
    with open('semaforo_dict.json', 'r') as file: semaforizacion_dict = json.load(file)
    rf_classifier = joblib.load('random_forest_cluster_predictor.joblib')
    preprocessor = joblib.load('preprocessor.joblib')
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

    print(f'El cluster predicho para los nuevos datos es: {predicted_cluster}')
    print(f'El semáforo correspondiente al cluster predicho es: {predicted_semaforo}')


if __name__ == '__main__':
    data = pd.read_excel('cluster_data/cluster_data.xlsx')  # Carga tu conjunto de datos
    with open('semaforo_dict.json', 'r') as file: semaforizacion_dict = json.load(file)

    work_data = data[['anio', 'provincia', 'comunidad_autonoma', 'cluster']]
    #predict_random_forest(work_data)
    test()