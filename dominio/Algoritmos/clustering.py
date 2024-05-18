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

def prepare_data(data):
    # Identificar las columnas categóricas y numéricas
    categorical_cols = ['provincia', 'comunidad_autonoma']
    numeric_cols = ['anio', 'accidentes_leves_jornada_por_persona', 'accidentes_graves_jornada_por_persona',
                    'accidentes_mortales_jornada_por_persona', 'accidentes_leves_itinere_por_persona',
                    'accidentes_graves_itinere_por_persona', 'accidentes_mortales_itinere_por_persona',
                    'accidentes_trafico_por_persona']

    # Transformación de columnas categóricas y numéricas
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(), categorical_cols)
        ])

    # Aplicar la transformación
    data_preprocessed = preprocessor.fit_transform(data)

    return data_preprocessed

def random_forest(data):
    data_preprocessed = prepare_data(data)
    # Paso 2: Entrenar un Random Forest
    # Generar etiquetas artificiales
    labels = np.random.randint(2, size=len(data))
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(data_preprocessed, labels)

    # Paso 3: Calcular la matriz de proximidad
    leaf_indices = rf.apply(data_preprocessed)
    proximity_matrix = np.zeros((len(data), len(data)))

    for i in range(len(data)):
        for j in range(i, len(data)):

            proximity_matrix[i, j] = np.sum(leaf_indices[i] == leaf_indices[j])
            proximity_matrix[j, i] = proximity_matrix[i, j]

    # Normalizar la matriz de proximidad
    proximity_matrix /= rf.n_estimators

    # Convertir la matriz de proximidad en una matriz de distancia
    distance_matrix = 1 - proximity_matrix

    return distance_matrix, rf

def hcluster_shilhoutte_analysis(data, new_rand_model=1, show_dend=0, show_shil=0, show_cluster_labels=0):
    cluster_summary = 0

    if new_rand_model == 0: distance_matrix= load_random_model(data)
    elif new_rand_model == 1: distance_matrix, rf = random_forest(data)

    distance_matrix_squareform = squareform(distance_matrix)
    Z = linkage(distance_matrix_squareform, method='ward')

    max_d_values = np.linspace(0.5, 2.0, 15)  # Ajusta el rango según sea necesario
    silhouette_scores = []
    data_results = []

    for max_d in max_d_values:
        clusters = fcluster(Z, max_d, criterion='distance')
        data['cluster'] = clusters
        silhouette_avg = silhouette_score(distance_matrix, clusters, metric='precomputed')
        silhouette_scores.append(silhouette_avg)
        data_results.append(data)

    if show_dend == 1: dendrograma(distance_matrix)
    if show_shil == 1:    
        plt.figure(figsize=(10, 6))
        plt.plot(max_d_values, silhouette_scores, marker='o')
        plt.title('Silhouette Scores para diferentes alturas de corte')
        plt.xlabel('Altura de corte (max_d)')
        plt.ylabel('Silhouette Score')
        plt.show()
    
    best_max_d = max_d_values[np.argmax(silhouette_scores)]
    best_data = data_results[np.argmax(silhouette_scores)]

    if show_shil == 1:  
        print(f'Mejor altura de corte: {best_max_d}')
        cluster_counts = best_data['cluster'].value_counts()
        for cluster, count in cluster_counts.items():
            print(f'Cluster {cluster}: {count}')

    cluster_summary = labels_info_cluster(best_data, show_cluster_labels)

    if new_rand_model == 1:
        if input('0. No guardar modelo\n1. Guardar modelo\nSeleccione: ') == '1':
            joblib.dump(rf, './random_forest_model_2.joblib')

    if input('0. No guardar resultado\n1. Guardar resultado\nSeleccione: ') == '1': create_excel(best_data, 'results/', 'cluster_3.xlsx')

    return best_data, cluster_summary

def dendrograma(distance_matrix):
    distance_matrix_squareform = squareform(distance_matrix)
    Z = linkage(distance_matrix_squareform, method='ward')

    plt.figure(figsize=(10, 7))
    plt.title("Dendograma del Clustering Jerárquico")
    dendrogram(Z)
    plt.xlabel('Índice de muestra')
    plt.ylabel('Distancia')
    plt.show()

def load_random_model(data):
    data_preprocessed = prepare_data(data)
    loaded_rf = joblib.load("./random_forest_model.joblib")
    # Paso 3: Calcular la matriz de proximidad
    leaf_indices = loaded_rf.apply(data_preprocessed)
    proximity_matrix = np.zeros((len(data), len(data)))

    for i in range(len(data)):
        for j in range(i, len(data)):

            proximity_matrix[i, j] = np.sum(leaf_indices[i] == leaf_indices[j])
            proximity_matrix[j, i] = proximity_matrix[i, j]

    # Normalizar la matriz de proximidad
    proximity_matrix /= loaded_rf.n_estimators

    # Convertir la matriz de proximidad en una matriz de distancia
    distance_matrix = 1 - proximity_matrix

    return distance_matrix

def labels_info_cluster(best_data, show_labels=0):
    # Filtrar solo columnas numéricas
    numeric_cols = best_data.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols.remove('cluster')
    
    # Realizar un análisis descriptivo de cada cluster
    cluster_summary = best_data.groupby('cluster')[numeric_cols].mean()
    
    if show_labels == 1:
        print("Resumen de los clusters:")
        print(cluster_summary)

        # Visualización de las características de los clusters
        num_plots = len(numeric_cols)
        num_cols = 3  # Número de gráficos por fila
        num_rows = (num_plots // num_cols) + (num_plots % num_cols > 0)

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
        axs = axs.flatten()
        fig.tight_layout(pad=5.0)

        for i, col in enumerate(numeric_cols):
            sns.boxplot(x='cluster', y=col, data=best_data, ax=axs[i], palette='viridis')
            axs[i].set_title(f'Boxplot de {col} por Cluster')
            axs[i].set_xlabel('Cluster')
            axs[i].set_ylabel(col)

        for j in range(i + 1, len(axs)):
            fig.delaxes(axs[j])

        plt.show()

        # Visualización de las características categóricas de los clusters
        categorical_cols = ['provincia', 'comunidad_autonoma']
        
        for col in categorical_cols:
            plt.figure(figsize=(10, 6))
            sns.countplot(x=col, hue='cluster', data=best_data, palette='viridis')
            plt.title(f'Frecuencia de {col} por Cluster')
            plt.xlabel(col)
            plt.ylabel('Frecuencia')
            plt.xticks(rotation=90)
            plt.legend(title='Cluster')
            plt.show()

    return cluster_summary

def hcluster(distance_matrix, max_d):
    distance_matrix_squareform = squareform(distance_matrix)
    Z = linkage(distance_matrix_squareform, method='ward')
    clusters = fcluster(Z, max_d, criterion='distance')
    data['cluster'] = clusters
    
    return data

def create_rank_clusters(cluster_summary):
    # Identificar las columnas categóricas y numéricas
    numeric_cols = ['accidentes_leves_jornada_por_persona', 'accidentes_graves_jornada_por_persona',
                    'accidentes_mortales_jornada_por_persona', 'accidentes_leves_itinere_por_persona',
                    'accidentes_graves_itinere_por_persona', 'accidentes_mortales_itinere_por_persona',
                    'accidentes_trafico_por_persona']

    # Transformación de columnas categóricas y numéricas
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), numeric_cols),
        ])
    
    # cluster_summary = pd.DataFrame(cluster_summary, columns=numeric_cols, index=cluster_summary.index)
    cluster_summary_scaled = preprocessor.fit_transform(cluster_summary)
    cluster_summary_scaled = pd.DataFrame(cluster_summary_scaled, columns=numeric_cols, index=cluster_summary.index)

    # Compute 'rank' column by summing up all the specified numeric columns per row
    cluster_summary['score'] = cluster_summary_scaled[numeric_cols].sum(axis=1)
    cluster_summary_sorted = cluster_summary.sort_values(by='score', ascending=False) # El score maximo que se puede obtener es 7 ya que es el numero de dimensiones numericas

    cluster_summary_sorted['rank'] = range(1, len(cluster_summary_sorted) + 1)
    cluster_rank = cluster_summary_sorted[['rank', 'score']]

    cluster_rank = cluster_rank.reset_index()
    print(cluster_rank)

    return cluster_rank

def semaforizacion(cluster_rank):
    scaler = MinMaxScaler()
    cluster_rank['score_scaled'] = scaler.fit_transform(cluster_rank[['score']])

    cluster_rank['semaforo'] = pd.cut(cluster_rank['score_scaled'], 
                                      bins=[-float('inf'), 0.33, 0.66, float('inf')], 
                                      labels=[3, 2, 1])
    print(cluster_rank)
    return cluster_rank


def create_excel(df, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    path = output_folder + file_name
    df.to_excel(path, index=False)

if __name__ == '__main__':
    data = pd.read_excel('C:/Users/garci/proyectos/cotizador/results/GOLD/gold2.xlsx')  # Carga tu conjunto de datos
    
    _, cluster_summary = hcluster_shilhoutte_analysis(data, new_rand_model=0, show_dend=0, show_shil=0, show_cluster_labels=0)
    cluster_rank = create_rank_clusters(cluster_summary)
    cluster_semaforo = semaforizacion(cluster_rank)