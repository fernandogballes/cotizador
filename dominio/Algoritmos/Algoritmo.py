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
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_samples, silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import KBinsDiscretizer

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

def estadisticas_cluster(df):
    df_cp = df.copy()
    cluster = kmeans_v2(df_cp,5,'')

    stats = cluster.groupby(['provincia', 'comunidad_autonoma']).agg({'cluster_': ['mean', 'var', 'std']}).reset_index()

    stats.columns = ['provincia', 'comunidad_autonoma', 'mean_cluster', 'var_cluster', 'std_cluster']

    return stats

def cluster_porcentual(df):
    df_copy= df.copy()

    df_copy['accidentes_jornada_por_persona'] = df_copy['total_accidentes_jornada']/df_copy['total_poblacion_ocupada_construccion']
    df_copy['accidentes_itinere_por_persona'] = df_copy['total_accidentes_itinere']/df_copy['total_poblacion_ocupada_construccion']
    df_copy['accidentes_trafico_por_persona'] = (df_copy['total_victimas_trafico'] * (df_copy['total_poblacion_ocupada_construccion']/df_copy['total_poblacion_activa'])) /df_copy['total_poblacion_ocupada_construccion']

    df_copy = df_copy[['anio', 'provincia', 'comunidad_autonoma', 'accidentes_jornada_por_persona', 'accidentes_itinere_por_persona', 'accidentes_trafico_por_persona']]
    df_copy = df_copy.sort_values(by=['accidentes_jornada_por_persona', 'accidentes_itinere_por_persona', 'accidentes_trafico_por_persona'], ascending=False)

    #print(df_copy.head(20), '\n\n', df_copy.tail(20))

    df2 = df_copy.copy()
    df2 = df2.groupby(['provincia', 'comunidad_autonoma']).agg({'accidentes_jornada_por_persona':'mean', 'accidentes_itinere_por_persona':'mean', 'accidentes_trafico_por_persona':'mean'}).reset_index()
    df2 = df2.sort_values(by=['accidentes_jornada_por_persona', 'accidentes_itinere_por_persona', 'accidentes_trafico_por_persona'], ascending=False)

    #print(df2.head(52))

    return df_copy, df2
    

def cluster_jerarquico(df):
    df_copy = df.copy()
    # Label Encoding para 'provincia' y 'comunidad_autonoma'
    label_encoder = LabelEncoder()
    df['provincia_encoded'] = label_encoder.fit_transform(df['provincia'])
    df['comunidad_autonoma_encoded'] = label_encoder.fit_transform(df['comunidad_autonoma'])

    # Seleccionar columnas numéricas para normalización
    columns_to_normalize = ['anio', 'total_poblacion_activa', 'total_poblacion_ocupada_construccion', 
                            'total_accidentes_jornada', 'leves_accidentes_jornada', 
                            'graves_accidentes_jornada', 'mortales_accidentes_jornada', 
                            'total_accidentes_itinere', 'leves_accidentes_itinere', 
                            'graves_accidentes_itinere', 'mortales_accidentes_itinere', 
                            'total_victimas_trafico']

    #columns_to_normalize = ['anio', 'provincia', 'comunidad_autonoma','accidentes_jornada_100000', 'accidentes_itinere_100000', 'accidentes_trafico_100000']

    # Normalización de las columnas numéricas
    scaler = StandardScaler()
    df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

    # Eliminar columnas originales
    df.drop(['provincia', 'comunidad_autonoma'], axis=1, inplace=True)

    # Aplicar clustering jerárquico
    X = df.values
    Z = linkage(X, method='ward', metric='euclidean')

    return Z, X

def dendograma(df):
    df_copy = df.copy()
    Z, X = cluster_jerarquico(df)
      
    # Obtener etiquetas para el eje x (año y provincia)
    etiquetas_x = [f"{anio} - {provincia}" for anio, provincia in zip(df_copy['anio'], df_copy['provincia'])]
    # Visualización del dendrograma con etiquetas personalizadas en el eje x
    plt.figure(figsize=(12, 8))
    dendrogram(Z, labels=etiquetas_x, orientation='top', leaf_font_size=10)
    plt.title('Dendrograma de Clustering Jerárquico')
    plt.xlabel('Elementos')
    plt.ylabel('Distancia')
    plt.xticks(rotation=90)  # Rotar etiquetas en el eje x para mejor visualización
    plt.tight_layout()
    plt.show()

def shilhoutte(df):
    df_copy = df.copy()
    Z, X = cluster_jerarquico(df)
    # Determinar el número óptimo de clusters utilizando el método de corte de dendrograma
    t = 4
    etiquetas_clusters = fcluster(Z, t=t, criterion='maxclust')

    # Calcular coeficientes de silueta
    coeficientes_silueta = silhouette_samples(X, etiquetas_clusters)
    coeficiente_silueta_promedio = silhouette_score(X, etiquetas_clusters)

    # Visualizar coeficientes de silueta
    plt.figure(figsize=(8, 6))
    plt.hist(coeficientes_silueta, bins=30, alpha=0.75, edgecolor='black')
    plt.axvline(x=coeficiente_silueta_promedio, color='red', linestyle='--', linewidth=2, label='Silhouette Score Promedio')
    plt.title('Distribución de Coeficientes de Silueta')
    plt.xlabel('Coeficiente de Silueta')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.show()

    print(f"El coeficiente de silueta promedio es: {coeficiente_silueta_promedio:.2f}")

def matriz_distancias(df):
    df_copy = df.copy()
    Z, X = cluster_jerarquico(df)
    # Calcular matriz de distancias
    distancias = linkage(X, method='ward', metric='euclidean')
    matriz_distancias = pd.DataFrame(distancias, columns=['cluster_1', 'cluster_2', 'distancia', 'n_elementos'])

    # Visualizar matriz de distancias como heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_distancias.pivot(index='cluster_1', columns='cluster_2', values='distancia'), cmap='viridis')
    plt.title('Heatmap de Matriz de Distancias')
    plt.xlabel('Cluster 2')
    plt.ylabel('Cluster 1')
    plt.show()

def caracteristicas_cluster(df):
    df_copy = df.copy()
    Z, X = cluster_jerarquico(df)
    t = 4  # Número de clusters deseado
    etiquetas_clusters = fcluster(Z, t=t, criterion='maxclust')

    # Agregar etiquetas de clusters al DataFrame original
    df['cluster'] = etiquetas_clusters

    # Análisis de características por cluster
    for cluster_id in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster_id].drop('cluster', axis=1)
        descripcion_cluster = cluster_data.describe()
        print(f'\nCluster {cluster_id}:')
        print(descripcion_cluster)


def reglas_asociacion(df):
    # Copiar el DataFrame original
    df_processed = df.copy()

    # Seleccionar las características numéricas para normalización y discretización
    numeric_features = ['total_poblacion_activa', 'total_poblacion_ocupada_construccion',
                        'total_accidentes_jornada', 'leves_accidentes_jornada',
                        'graves_accidentes_jornada', 'mortales_accidentes_jornada',
                        'total_accidentes_itinere', 'leves_accidentes_itinere',
                        'graves_accidentes_itinere', 'mortales_accidentes_itinere',
                        'total_victimas_trafico']

    # Normalizar las características numéricas
    scaler = StandardScaler()
    df_processed[numeric_features] = scaler.fit_transform(df_processed[numeric_features])

    # Discretizar las características numéricas
    discretizer = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')  # Puedes ajustar los parámetros según sea necesario
    df_processed[numeric_features] = discretizer.fit_transform(df_processed[numeric_features])

    # Seleccionar características discretizadas y otras columnas relevantes
    df_items = df_processed[['anio', 'provincia', 'comunidad_autonoma'] + numeric_features]

    # Convertir características numéricas discretizadas en variables categóricas
    df_items = pd.get_dummies(df_items, columns=numeric_features, prefix=numeric_features)

    # Convertir todas las columnas a tipo booleano
    df_items = df_items.astype(bool)

    # Aplicar el algoritmo Apriori para encontrar conjuntos frecuentes
    frequent_itemsets = apriori(df_items, min_support=0.1, use_colnames=True)

    # Generar reglas de asociación a partir de los conjuntos frecuentes
    rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1.0)

    # Mostrar las reglas de asociación encontradas
    print("Reglas de Asociación:")
    rules.to_csv('results/GOLD/rules.csv', index=False)

def multiply_columns(df):
    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    columnas_numericas = columnas_numericas.drop(['anio','porcentaje_poblacion_ocupada_construccion'])
    df = df.drop('porcentaje_poblacion_ocupada_construccion', axis=1)
    df[columnas_numericas] *= 1000

    return df


def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

if __name__ == '__main__':
    df = pd.read_excel('results/GOLD/gold.xlsx')
    df = multiply_columns(df)

    # CLUSTER CON ACCIDENTES POR PERSONA DE COSNTRUCCION
    """ df_por_persona_no_agrupado, df_por_persona_agrupado = cluster_porcentual(df) """

    """ df_por_persona_no_agrupado = df_por_persona_no_agrupado.sort_values(by=['anio', 'provincia'])
    df_por_persona_no_agrupado = df_por_persona_no_agrupado[df_por_persona_no_agrupado['anio']>2008]
    sns.lineplot(x='anio', y='accidentes_jornada_por_persona', hue='provincia', data=df_por_persona_no_agrupado)
    plt.legend(loc='upper left')
    plt.show() """

    """ cluster_por_persona_no_agrupado = kmeans_v2(df_por_persona_no_agrupado, 3, 'por_persona_no_agrupado')
    cluster_por_persona_agrupado = kmeans_v2(df_por_persona_agrupado, 3, 'por_persona_agrupado')

    print(cluster_por_persona_no_agrupado.head(50))
    print(cluster_por_persona_agrupado.head(52)) """

    """ stats = estadisticas_cluster(df)
    print(stats) """

    #df = create_ratios_100000(df)
    # cluster_jerarquico(df)

    # REGLAS DE ASOCIACION
    """ reglas_asociacion(df.copy()) """

    # CLUSTER JERARQUICO
    """ dendograma(df.copy())
    shilhoutte(df.copy())
    matriz_distancias(df.copy())
    caracteristicas_cluster(df.copy())
 """

    # TOTAL DF OPTIONS
    """ total_df = create_all_df(df)
    create_excel(total_df, 'results/GOLD/', 'all_df_options.xlsx') """

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

   
