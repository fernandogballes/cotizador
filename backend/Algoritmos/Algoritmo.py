import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.plotting import scatter_matrix
from scipy.stats import pearsonr, randint as sp_randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_absolute_error, precision_score
# Imports Decision Tree
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.model_selection import KFold
#Imports naive bayes
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
#Imports K-MEANS
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import LabelEncoder


def create_danger_index():
    df = pd.read_excel('results/GOLD/gold.xlsx')

    df = df[['anio', 'provincia', 'comunidad_autonoma', 'total_accidentes_jornada', 'total_victimas_trafico', 'porcentaje_poblacion_ocupada', 'total_accidentes_itinere']]

    df['danger_num'] = (df['total_accidentes_jornada']*0.5 + df['total_victimas_trafico'] * df['porcentaje_poblacion_ocupada'] * 0.15 + df['total_accidentes_itinere'] * 0.35)/3

    #list_ccmm = ['asturias', 'cantabria', 'navarra', 'la rioja', 'pais vasco', 'murcia', 'baleares', 'canarias', 'ceuta', 'melilla']
    list_ccmm = ['andalucia', 'aragon' 'castilla la mancha', 'castilla y leon', 'cataluna', 'comunidad valenciana', 'extremadura', 'galicia', 'madrid']

    df_1 = df[df['comunidad_autonoma']!=df['provincia']]
    df_2 = df[~df['comunidad_autonoma'].isin(list_ccmm)].copy()

    df_prov_uniccmm = pd.concat([df_1, df_2])
    df_comunidades_grandes = df[df['comunidad_autonoma'].isin(list_ccmm)].copy()

    comunidades_danger_num = df_comunidades_grandes['danger_num']
    provincias_danger_num = df_prov_uniccmm['danger_num']

    comunidades_min_value = min(comunidades_danger_num)
    comunidades_range_value = max(comunidades_danger_num) - comunidades_min_value

    provincias_min_value = min(provincias_danger_num)
    provincias_range_value = max(provincias_danger_num) - provincias_min_value
    
    comunidades_normalized_list = [(valor - comunidades_min_value) / comunidades_range_value for valor in comunidades_danger_num]
    provincias_normalized_list = [(valor - provincias_min_value) / provincias_range_value for valor in provincias_danger_num]

    df_comunidades_grandes['danger_index'] = comunidades_normalized_list
    df_prov_uniccmm['danger_index'] = provincias_normalized_list

    result_df = pd.concat([df_comunidades_grandes, df_prov_uniccmm])
    result_df = result_df.drop('danger_num', axis=1)
    
    result_df.sort_values(by=['anio', 'comunidad_autonoma'], inplace=True)

    """ print(result_df.head(20))
    print(result_df[(result_df['comunidad_autonoma'].isin(list_ccmm) & (result_df['comunidad_autonoma']==result_df['provincia']) & (result_df['anio']==2012))])
    print('\n\n\n', result_df[(result_df['danger_index']==max(result_df['danger_index']))]) """

    result_df = result_df[['anio', 'provincia', 'comunidad_autonoma', 'danger_index']].copy()

    return result_df

def encoder_scaler(df):
    df_codec = df.copy()

    label_encoder = LabelEncoder()

    df_codec['provincia'] = label_encoder.fit_transform(df_codec['provincia'])
    df_codec['comunidad_autonoma'] = label_encoder.fit_transform(df_codec['comunidad_autonoma'])

    X = df_codec[['anio', 'provincia', 'comunidad_autonoma', 'danger_index']]

    # Escala los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled

def kmeans(df):
    X_scaled = encoder_scaler(df)

    kmeans = KMeans(n_clusters=3, random_state=50)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Muestra el DataFrame con la columna de clusters
    print(df)

    # Puedes visualizar los resultados si lo deseas
    plt.scatter(df['anio'], df['danger_index'], c=df['cluster'], cmap='viridis')
    plt.xlabel('Año')
    plt.ylabel('Danger Index')
    plt.title('K-means Clustering')
    plt.show()

def elbow_method(df_codec):
    X_scaled = encoder_scaler(df_codec)
    # Realiza el método del codo para determinar el número óptimo de clusters
    inertia = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    # Grafica el método del codo
    plt.plot(range(1, 11), inertia, marker='o')
    plt.xlabel('Número de Clusters')
    plt.ylabel('Inertia (Suma de cuadrados intra-cluster)')
    plt.title('Método del Codo')
    plt.show()


if __name__ == '__main__':
    kmeans(create_danger_index())