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

def create_danger_index():
    df = pd.read_excel('results/GOLD/gold.xlsx')

    df['danger_num'] = (df['total_accidentes_jornada']*0.5 + df['total_victimas_trafico'] * df['porcentaje_poblacion_ocupada_construccion'] * 0.15 + df['total_accidentes_itinere'] * 0.35)/1

    df_normalized_list = [(valor - min(df['danger_num'])) / (max(df['danger_num']) - min(df['danger_num'])) for valor in df['danger_num']]
    df['danger_index'] = df_normalized_list

    return df

def create_ratios(df):
    df['ratio_leves_totales_jornada'] = np.divide(df['leves_accidentes_jornada'], df['total_accidentes_jornada'], out=np.zeros_like(df['total_accidentes_jornada']), where=df['total_accidentes_jornada'] != 0) 
    df['ratio_graves_totales_jornada'] = np.divide(df['graves_accidentes_jornada'], df['total_accidentes_jornada'], out=np.zeros_like(df['total_accidentes_jornada']), where=df['total_accidentes_jornada'] != 0)
    df['ratio_mortales_totales_jornada'] = np.divide(df['mortales_accidentes_jornada'], df['total_accidentes_jornada'], out=np.zeros_like(df['total_accidentes_jornada']), where=df['total_accidentes_jornada'] != 0)

    df['ratio_leves_totales_itinere'] = np.divide(df['leves_accidentes_itinere'], df['total_accidentes_itinere'], out=np.zeros_like(df['total_accidentes_itinere']), where=df['total_accidentes_itinere'] != 0)
    df['ratio_graves_totales_itinere'] = np.divide(df['graves_accidentes_itinere'], df['total_accidentes_itinere'], out=np.zeros_like(df['total_accidentes_itinere']), where=df['total_accidentes_itinere'] != 0)
    df['ratio_mortales_totales_itinere'] = np.divide(df['mortales_accidentes_itinere'], df['total_accidentes_itinere'], out=np.zeros_like(df['total_accidentes_itinere']), where=df['total_accidentes_itinere'] != 0)

    df['ratio_accidentes_itinere_accidentes_trafico'] = np.divide(df['total_accidentes_itinere'], df['total_victimas_trafico'], out=np.zeros_like(df['total_victimas_trafico']), where=df['total_victimas_trafico'] != 0)

    df['ratio_accidentes_jornada_ocupados'] = np.divide(df['total_accidentes_jornada'], df['total_poblacion_ocupada_construccion'], out=np.zeros_like(df['total_poblacion_ocupada_construccion']), where=df['total_poblacion_ocupada_construccion'] != 0)
    df['ratio_accidentes_itinere_ocupados'] = np.divide(df['total_accidentes_itinere'], df['total_poblacion_ocupada_construccion'], out=np.zeros_like(df['total_poblacion_ocupada_construccion']), where=df['total_poblacion_ocupada_construccion'] != 0)

    return df

def create_df_of_ratios(df):
    cols = df.columns
    selected_columns = ['anio', 'provincia', 'comunidad_autonoma']
    ratio_columns = list(filter(lambda x: 'ratio' in x, cols))

    selected_columns = selected_columns + ratio_columns

    df_filtered = df[selected_columns]

    return df_filtered

def normalize_ratios(df):
    cols = df.columns
    ratio_columns = list(filter(lambda x: 'ratio' in x, cols))

    df[ratio_columns] = (df[ratio_columns] - df[ratio_columns].min()) / (df[ratio_columns].max() - df[ratio_columns].min())

    return df

def create_score(df):
    ratio_columns = df.filter(like='ratio')

    df['score'] = ratio_columns.mean(axis=1, skipna=True)

    df.sort_values(by=['anio', 'score'], inplace=True)
    
    return df

def create_rank(df):
    df['rank'] = df.groupby('anio')['score'].rank(ascending=False)
    return df

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

def dbscan(df):
    #X_scaled = encoder_scaler(df)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    eps_values = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    min_samples_values = [5, 10, 50]

    results = []

    for eps in eps_values:
        for min_samples in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            clusters = dbscan.fit_predict(X_scaled)
            inertia = pairwise_distances(X_scaled, metric='euclidean', squared=True).min(axis=1).sum()

            results.append({'eps': eps, 'min_samples': min_samples, 'inertia': inertia})

    eps_values = [res['eps'] for res in results]
    min_samples_values = [res['min_samples'] for res in results]
    inertia_values = [res['inertia'] for res in results]

    # Crear un gráfico 3D para visualizar la relación entre eps, min_samples y la inercia
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(eps_values, min_samples_values, inertia_values, c='r', marker='o')

    ax.set_xlabel('Eps')
    ax.set_ylabel('Min Samples')
    ax.set_zlabel('Inertia')

    plt.show()

def neuronal_network(df):
    X_scaled = encoder_scaler(df)  
    y = df['danger_index']  
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    model = keras.Sequential([
      layers.Dense(4, activation='relu'),
      layers.Dense(4, activation='relu'),
      layers.Dense(1, activation = 'linear')
      ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose = 0) # verbose=0

    predictions = model.predict(X_test)
    predictions = predictions.flatten()
    y_pred = predictions

    mae_dict_1 = metrics.mean_absolute_error(y_test, y_pred)
    r2_dict_1 =  metrics.r2_score(y_test, y_pred)
    print(f"MAE = {mae_dict_1}, R^2 = {r2_dict_1}")

    model.save('results/red_neuronal')

    return 1

def neuronal_network_3(df):
    # NORMALIZACION
    cols = df.columns
    total_columns = list(filter(lambda x: 'total' in x, cols))
    df[total_columns] = (df[total_columns] - df[total_columns].min()) / (df[total_columns].max() - df[total_columns].min())
    #df[total_columns] = df[total_columns] * (df[total_columns].max() - df[total_columns].min()) + df[total_columns].min() #DESNORMALIZACION

    x = df.drop(['total_accidentes_jornada', 'total_accidentes_itinere', 'total_victimas_trafico'], axis=1)

    X_scaled = encoder_scaler(x)  
    y1 = df['total_accidentes_jornada'] 
    y2 = df['total_accidentes_itinere']  
    y3 = df['total_victimas_trafico']  

    X_train, X_test, y1_train, y1_test, y2_train, y2_test, y3_train, y3_test = train_test_split(X_scaled, y1, y2, y3, test_size=0.3, random_state=42)

    model = keras.Sequential([
      layers.Dense(8, activation='relu'),
      layers.Dense(8, activation='relu'),
      layers.Dense(8, activation='relu'),
      layers.Dense(3, activation='sigmoid') 
      ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    model.fit(X_train, [y1_train, y2_train, y3_train], epochs=50, batch_size=32, validation_data=(X_test, [y1_test, y2_test, y3_test]), verbose=0)

    predictions = model.predict(X_test)
    y1_pred = predictions[:, 0]
    y2_pred = predictions[:, 1]
    y3_pred = predictions[:, 2]


    mae_dict_1 = metrics.mean_absolute_error(y1_test, y1_pred)
    mae_dict_2 = metrics.mean_absolute_error(y2_test, y2_pred)
    mae_dict_3 = metrics.mean_absolute_error(y3_test, y3_pred)
    r2_dict_1 =  metrics.r2_score(y1_test, y1_pred)
    r2_dict_2 =  metrics.r2_score(y2_test, y2_pred)
    r2_dict_3 =  metrics.r2_score(y3_test, y3_pred)
    
    print(f"MAE columna 1 = {mae_dict_1}, R^2 columna 1 = {r2_dict_1}")
    print(f"MAE columna 2 = {mae_dict_2}, R^2 columna 2 = {r2_dict_2}")
    print(f"MAE columna 3 = {mae_dict_3}, R^2 columna 3 = {r2_dict_3}")

    model.save('results/red_neuronal_2')

    return 1

def predict_NN3(anios, provincias, comunidades_autonomas):

    data = {'anio': anios, 'provincia': provincias, 'comunidad_autonoma': comunidades_autonomas}
    df = pd.DataFrame(data) 

    df_scaled = encoder_scaler(df)

    model = keras.models.load_model('results/red_neuronal_2')
    predictions = model.predict(df_scaled)

    return df, predictions

def desnormalization(df, data, pred):
    columns_order = ['total_accidentes_jornada', 'total_accidentes_itinere', 'total_victimas_trafico']

    pred_df = pd.DataFrame(pred, columns=columns_order)
    
    # Desnormalizar las predicciones
    desnormalized_pred = pred_df[columns_order] * (df[columns_order].max() - df[columns_order].min()) + df[columns_order].min()    
    result_df = data.join(desnormalized_pred)
    
    return result_df

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

def elbow_pca(df):
    label_encoder = LabelEncoder()
    # Codificar las columnas de string
    df['comunidad_autonoma_encoded'] = label_encoder.fit_transform(df['comunidad_autonoma'])
    df['provincia_encoded'] = label_encoder.fit_transform(df['provincia'])
    df = df.drop(['comunidad_autonoma', 'provincia'], axis = 1)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    pca = PCA()
    pca.fit(scaled_data)

    # Obtener la varianza explicada acumulativa
    explained_variance_ratio = np.cumsum(pca.explained_variance_ratio_)

    # Graficar la varianza explicada acumulativa
    plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, marker='o')
    plt.xlabel('Número de Componentes')
    plt.ylabel('Varianza Explicada Acumulativa')
    plt.title('Método del Codo para determinar el número de componentes en PCA')
    plt.grid(True)
    plt.show()

def apply_pca(df):
    label_encoder = LabelEncoder()
    # Codificar las columnas de string
    df['comunidad_autonoma_encoded'] = label_encoder.fit_transform(df['comunidad_autonoma'])
    df['provincia_encoded'] = label_encoder.fit_transform(df['provincia'])
    df = df.drop(['comunidad_autonoma', 'provincia'], axis = 1)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(scaled_data)

    # Crear un nuevo DataFrame con los resultados del PCA
    pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2', 'PC3'])

    return pca_df

def mean_cluster_provincia(df):
    # Agrupar por provincia y calcular la media del cluster
    df_media_clusters = df.groupby('provincia')['cluster'].mean().reset_index()

    df_media_clusters['cluster'] = round(df_media_clusters['cluster'])
    # df_media_clusters['cluster'] = np.ceil(df_media_clusters['cluster'])
    # df_media_clusters['cluster'] = df_media_clusters['cluster'].apply(lambda x: Decimal(x).quantize(0, ROUND_HALF_UP))
    # df_media_clusters['cluster'] = df_media_clusters['cluster'].apply(lambda x: Decimal(x).quantize(0, ROUND_HALF_DOWN))
    # df_cluster_comun = df.groupby('provincia')['cluster'].agg(lambda x: x.value_counts().index[0]).reset_index()

    return df_media_clusters

def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

if __name__ == '__main__':
    df = pd.read_excel('results/GOLD/gold.xlsx')

    clustering = kmeans(df)
    clustering = mean_cluster_provincia(clustering)
    print(clustering)
    create_excel(clustering, 'results/GOLD/', 'provincias_clustering.xlsx')


    # CORRELACION DE VARIABLES ORGINALES
    """ heat_map(df)

    # ESTUDIO DEL PCA
    elbow_pca(df)

    # CLUSTER CON PCA
    pca = apply_pca(df)
    kmeans(pca) """

    # DBSCAN CON PCA
    """ pca = apply_pca(df)
    dbscan(pca) """

    # DF SIMPLIFICADO EN BASE A LAS CORRELACIONES
    """ df = df[['anio', 'provincia', 'comunidad_autonoma', 'total_accidentes_jornada', 'total_accidentes_itinere', 'total_victimas_trafico']] """

    # ENTRENAR NN
    """ neuronal_network_3(df) """

    # USAR NN
    """ anios = ['2019']
    provincias = ['alicante']
    comunidades_autonomas = ['comunidad valenciana']
    data, pred = predict_NN3(anios, provincias, comunidades_autonomas)
    pred_df = desnormalization(df, data, pred)
    print(pred_df)

    cols = df.columns
    total_columns = list(filter(lambda x: 'total' in x, cols))
    df[total_columns] = (df[total_columns] - df[total_columns].min()) / (df[total_columns].max() - df[total_columns].min())
    print(df[(df['anio']==2019) & (df['provincia']=='alicante') & (df['comunidad_autonoma']=='comunidad valenciana')]) """

    #CREACION DE RATIOS Y DATAFRAME SOLO RATIOS
    """ df = create_ratios(df)
    df = create_df_of_ratios(df) """

    # CORRELACION DE RATIOS
    """ heat_map(df) """
    # NORMALIZACION DE LOS DATOS Y CORRELACION
    """ df = normalize_ratios(df)
    heat_map(df) """

    # SCORE Y RANGO EN BASE A LOS RATIOS
    """ df = create_score(df)
    df2 = create_rank(df) """