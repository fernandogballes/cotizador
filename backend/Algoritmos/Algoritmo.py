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

def create_danger_index():
    df = pd.read_excel('results/GOLD/gold.xlsx')

    df['danger_num'] = (df['total_accidentes_jornada']*0.5 + df['total_victimas_trafico'] * df['porcentaje_poblacion_ocupada_construccion'] * 0.15 + df['total_accidentes_itinere'] * 0.35)/3

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

    X = df_codec[['anio', 'provincia', 'comunidad_autonoma', 'danger_index']]

    # Escala los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled

def kmeans(df):
    X_scaled = encoder_scaler(df)

    kmeans = KMeans(n_clusters=3, random_state=50)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    print(df)

    plt.scatter(df['anio'], df['danger_index'], c=df['cluster'], cmap='viridis')
    plt.xlabel('Año')
    plt.ylabel('Danger Index')
    plt.title('K-means Clustering')
    plt.show()

def elbow_method(df_codec):
    X_scaled = encoder_scaler(df_codec)
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
    X_scaled = encoder_scaler(df)
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

    # Filtrar correlaciones mayores a 0.6
    correlations_above_06 = corr_matrix[abs(corr_matrix) > 0.5].stack().dropna()
    correlations_above_06 = correlations_above_06[correlations_above_06 != 1]  # Eliminar correlaciones con sí mismas

    # Filtrar correlaciones únicas
    unique_correlations = correlations_above_06.reset_index()
    unique_correlations = unique_correlations[unique_correlations['level_0'] < unique_correlations['level_1']]

    # Guardar las correlaciones únicas en un archivo de texto
    unique_correlations.to_csv('correlaciones_superiores_06.txt', header=None, sep=' ', index=False)

    # Imprimir mensaje de confirmación
    print("Correlaciones superiores a 0.6 y únicas guardadas en 'correlaciones_superiores_06.txt'.")


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


if __name__ == '__main__':
    df = pd.read_excel('results/GOLD/gold.xlsx')
    #df = create_danger_index()
    elbow_pca(df)
    #heat_map(df)
    df = create_ratios(df)
    df = create_df_of_ratios(df)
    heat_map(df)
    df = normalize_ratios(df)
    #heat_map(df)

    # SCORE Y RANGO
    df = create_score(df)
    df2 = create_rank(df)
    