import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances
from tensorflow import keras
from keras import layers
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
import os
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN

def encoder_scaler(df):
    df_codec = df.copy()

    label_encoder = LabelEncoder()

    df_codec['provincia'] = label_encoder.fit_transform(df_codec['provincia'])
    df_codec['comunidad_autonoma'] = label_encoder.fit_transform(df_codec['comunidad_autonoma'])

    #X = df_codec[['anio', 'provincia', 'comunidad_autonoma', 'danger_index']]
    X = df_codec

    # Escala los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled

def kmeans(df):
    X_scaled = encoder_scaler(df)
    """ scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df) """

    # Aplicar K-means
    kmeans = KMeans(n_clusters=3, random_state=50)
    clusters = kmeans.fit_predict(X_scaled)

    # Añadir los clusters al DataFrame
    df['cluster'] = clusters

    """ # Seleccionar dos características para graficar
    feature1 = df.columns[0]  # Selecciona la primera característica
    feature2 = df.columns[1]  # Selecciona la segunda característica

    # Graficar los clusters
    plt.figure(figsize=(10, 6))
    plt.scatter(df[feature1], df[feature2], c=clusters, cmap='viridis', alpha=0.5)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.title('Clusters obtenidos mediante K-means')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    plt.show() """

    return df

def elbow_method(df_codec):
    #X_scaled = encoder_scaler(df_codec)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_codec)
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

def heat_map(df):
    label_encoder = LabelEncoder()

    # Codificar las columnas de string
    df['comunidad_autonoma_encoded'] = label_encoder.fit_transform(df['comunidad_autonoma'])
    df['provincia_encoded'] = label_encoder.fit_transform(df['provincia'])

    df = df.drop(['comunidad_autonoma', 'provincia'], axis = 1)
    corr_matrix = df.corr()
    # Crear el mapa de calor
    plt.figure(figsize=(8, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Mapa de Calor')
    plt.tight_layout()
    plt.show()

    """ corr_table = corr_matrix.stack().reset_index()
    corr_table.columns = ['Variable_1', 'Variable_2', 'Correlacion']
    corr_table.to_csv('correlation_table.csv', index=False) """

    """ # Filtrar correlaciones mayores a 0.6
    correlations_above_06 = corr_matrix[abs(corr_matrix) > 0.5].stack().dropna()
    correlations_above_06 = correlations_above_06[correlations_above_06 != 1]  # Eliminar correlaciones con sí mismas

    # Filtrar correlaciones únicas
    unique_correlations = correlations_above_06.reset_index()
    unique_correlations = unique_correlations[unique_correlations['level_0'] < unique_correlations['level_1']]

    # Guardar las correlaciones únicas en un archivo de texto
    unique_correlations.to_csv('correlaciones_superiores_06.txt', header=None, sep=' ', index=False)

    # Imprimir mensaje de confirmación """

def mean_cluster_provincia(df):
    # Agrupar por provincia y calcular la media del cluster
    df_media_clusters = df.groupby('provincia')['cluster'].mean().reset_index()

    df_media_clusters['cluster'] = round(df_media_clusters['cluster'])
    # df_media_clusters['cluster'] = np.ceil(df_media_clusters['cluster'])
    # df_media_clusters['cluster'] = df_media_clusters['cluster'].apply(lambda x: Decimal(x).quantize(0, ROUND_HALF_UP))
    # df_media_clusters['cluster'] = df_media_clusters['cluster'].apply(lambda x: Decimal(x).quantize(0, ROUND_HALF_DOWN))
    # df_cluster_comun = df.groupby('provincia')['cluster'].agg(lambda x: x.value_counts().index[0]).reset_index()

    return df_media_clusters

def accidentes_100000(df):
    df['accidentes_10000'] = (df['total_accidentes_jornada']/df['total_poblacion_activa']*100000) + (df['total_accidentes_itinere']/df['total_poblacion_activa']*100000) + (df['total_victimas_trafico']/df['total_poblacion_activa']*100000)
    df_media_ratio = df.groupby('provincia')['accidentes_10000'].mean().reset_index()

    df_media_ratio = df_media_ratio.sort_values(by='accidentes_10000')
    cuartiles = df_media_ratio['accidentes_10000'].quantile([0.4, 0.8])
    df_media_ratio['cuartil'] = pd.cut(df_media_ratio['accidentes_10000'], bins=[-float('inf'), cuartiles.iloc[0], cuartiles.iloc[1], float('inf')], labels=['1', '2', '3'])

    return df_media_ratio

def ratios_100000(df):
    df['accidentes_jornada_100000'] = df['total_accidentes_jornada']/df['total_poblacion_activa']*100000
    df['accidentes_itinere_100000'] = df['total_accidentes_itinere']/df['total_poblacion_activa']*100000
    df['accidentes_trafico_100000'] = df['total_victimas_trafico']/df['total_poblacion_activa']*100000

    df_media_ratios = df.groupby('provincia').agg({'accidentes_jornada_100000': 'mean', 'accidentes_itinere_100000': 'mean', 'accidentes_trafico_100000': 'mean'}).reset_index()

    label_encoder = LabelEncoder()
    df_media_ratios['provincia'] = label_encoder.fit_transform(df_media_ratios['provincia'])
    X = df_media_ratios.drop(columns=['provincia'])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=2, random_state=50)
    clusters = kmeans.fit_predict(X_scaled)
    df_media_ratios['cluster'] = clusters
    df_media_ratios['provincia'] = label_encoder.inverse_transform(df_media_ratios['provincia'])

    return df_media_ratios

def create_ratios_100000(df):
    df['accidentes_jornada_100000'] = df['total_accidentes_jornada']/df['total_poblacion_activa']*100000
    df['accidentes_itinere_100000'] = df['total_accidentes_itinere']/df['total_poblacion_activa']*100000
    df['accidentes_trafico_100000'] = df['total_victimas_trafico']/df['total_poblacion_activa']*100000

    df = df[['anio', 'provincia', 'comunidad_autonoma','accidentes_jornada_100000', 'accidentes_itinere_100000', 'accidentes_trafico_100000']]

    return df

def grouped_ratios_100000(df):
    df_media_ratios = df.groupby(['provincia', 'comunidad_autonoma']).agg({'cluster': 'mean','accidentes_jornada_100000': 'mean', 'accidentes_itinere_100000': 'mean', 'accidentes_trafico_100000': 'mean'}).reset_index()
    df_media_ratios['cluster'] = df_media_ratios['cluster'].apply(lambda x: Decimal(x).quantize(0, ROUND_HALF_DOWN))
    return df_media_ratios

def cluster_100000(df):
    df_ratios_100000 = create_ratios_100000(df)
    # df_grouped_ratios_100000 = grouped_ratios_100000(df_ratios_100000)
    cluster_df = kmeans(df_ratios_100000)
    df_grouped_ratios_100000 = grouped_ratios_100000(cluster_df)
    create_excel(df_grouped_ratios_100000, 'results/GOLD/', 'provincias_clustering_v3.xlsx')
    create_excel(df_ratios_100000, 'results/GOLD/', 'provincias_clustering_anual.xlsx')


def create_all_df(df_no_ratio_no_grouped):
    # PRE CLUSTER
    df_ratio_no_grouped = create_ratios_100000(df_no_ratio_no_grouped)

    col_drop = ['anio']
    df_no_ratio_grouped = df_no_ratio_no_grouped.drop(col_drop, axis=1).groupby(['provincia', 'comunidad_autonoma']).mean().reset_index()
    df_no_ratio_no_grouped = df_no_ratio_no_grouped.drop(col_drop, axis=1)
    df_ratio_no_grouped = df_ratio_no_grouped.drop(col_drop, axis=1)


    df_ratio_grouped =  df.groupby(['provincia', 'comunidad_autonoma']).agg({'accidentes_jornada_100000': 'mean', 'accidentes_itinere_100000': 'mean', 'accidentes_trafico_100000': 'mean'}).reset_index()

    # POST CLUSTER
    df_ratio_no_grouped_cluster_2 = kmeans_v2(df_ratio_no_grouped, 2, 'df_ratio_no_grouped_cluster_2')
    df_ratio_no_grouped_cluster_3 = kmeans_v2(df_ratio_no_grouped, 3, 'df_ratio_no_grouped_cluster_3')

    df_no_ratio_no_grouped_cluster_2 = kmeans_v2(df_no_ratio_no_grouped, 2, 'df_no_ratio_no_grouped_cluster_2')
    df_no_ratio_no_grouped_cluster_3 = kmeans_v2(df_no_ratio_no_grouped, 3, 'df_no_ratio_no_grouped_cluster_3')

    df_ratio_grouped_cluster_2 = kmeans_v2(df_ratio_grouped, 2, 'df_ratio_grouped_cluster_2')
    df_ratio_grouped_cluster_3 = kmeans_v2(df_ratio_grouped, 3, 'df_ratio_grouped_cluster_3')

    df_no_ratio_grouped_cluster_2 = kmeans_v2(df_no_ratio_grouped, 2, 'df_no_ratio_grouped_cluster_2')
    df_no_ratio_grouped_cluster_3 = kmeans_v2(df_no_ratio_grouped, 3, 'df_no_ratio_grouped_cluster_3')

    # AGRUPAR LOS NO GROUPED
    df_ratio_no_grouped_cluster_2 = df_ratio_no_grouped_cluster_2.groupby(['provincia', 'comunidad_autonoma']).mean().reset_index()
    df_ratio_no_grouped_cluster_3 = df_ratio_no_grouped_cluster_3.groupby(['provincia', 'comunidad_autonoma']).mean().reset_index()

    df_no_ratio_no_grouped_cluster_2 = df_no_ratio_no_grouped_cluster_2.groupby(['provincia', 'comunidad_autonoma']).mean().reset_index()
    df_no_ratio_no_grouped_cluster_3 = df_no_ratio_no_grouped_cluster_3.groupby(['provincia', 'comunidad_autonoma']).mean().reset_index()

    df_ratio_no_grouped_cluster_2['cluster_df_ratio_no_grouped_cluster_2'] = round(df_ratio_no_grouped_cluster_2['cluster_df_ratio_no_grouped_cluster_2'])
    df_ratio_no_grouped_cluster_3['cluster_df_ratio_no_grouped_cluster_3'] = round(df_ratio_no_grouped_cluster_3['cluster_df_ratio_no_grouped_cluster_3'])
    df_no_ratio_no_grouped_cluster_2['cluster_df_no_ratio_no_grouped_cluster_2'] = round(df_no_ratio_no_grouped_cluster_2['cluster_df_no_ratio_no_grouped_cluster_2'])
    df_no_ratio_no_grouped_cluster_3['cluster_df_no_ratio_no_grouped_cluster_3'] = round(df_no_ratio_no_grouped_cluster_3['cluster_df_no_ratio_no_grouped_cluster_3'])

    # ['provincia', 'comunidad_autonoma', 'accidentes_jornada_100000', 'accidentes_itinere_100000', 'accidentes_trafico_100000']
    merged_df = df_ratio_no_grouped_cluster_2.merge(df_ratio_no_grouped_cluster_3, how='inner') \
        .merge(df_no_ratio_no_grouped_cluster_2, how='inner') \
        .merge(df_no_ratio_no_grouped_cluster_3, how='inner') \
        .merge(df_ratio_grouped_cluster_2, how='inner') \
        .merge(df_ratio_grouped_cluster_3, how='inner') \
        .merge(df_no_ratio_grouped_cluster_2, how='inner') \
        .merge(df_no_ratio_grouped_cluster_3, how='inner')

    return merged_df

def kmeans_v2(df, num_cluster, name):
    df_copy = df.copy()
    X_scaled = encoder_scaler(df_copy)

    kmeans = KMeans(n_clusters=num_cluster, random_state=50)
    clusters = kmeans.fit_predict(X_scaled)

    col_name = 'cluster_' + name
    df_copy[col_name] = clusters

    return df_copy

def multiply_columns(df):
    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    df[columnas_numericas] *= 1000
    df = df.drop('porcentaje_poblacion_ocupada_construccion', axis=1)

    return df


def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

if __name__ == '__main__':
    df = pd.read_excel('results/GOLD/gold.xlsx')
    df = multiply_columns(df)

    # TOTAL DF OPTIONS
    total_df = create_all_df(df)
    create_excel(total_df, 'results/GOLD/', 'all_df_options.xlsx')

    # DASHBOARD 3
    """ cluster_100000(df) """

    # DASHBOARD 2
    """ result_df = ratios_100000(df)
    create_excel(result_df, 'results/GOLD/', 'provincias_clustering_v2.xlsx') """

    # DASHBOARD 1
    """ clustering = kmeans(df)
    clustering = mean_cluster_provincia(clustering)
    df_ratio = accidentes_100000(df)

    df_merged = pd.merge(clustering, df_ratio, on='provincia', how='left')

    create_excel(df_merged, 'results/GOLD/', 'provincias_clustering.xlsx') """