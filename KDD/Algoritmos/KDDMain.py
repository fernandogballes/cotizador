import Clustering as Cluster
import Prediction as Predict

if __name__ == '__main__':
    print('Creando clusters y semaforización...\n')
    Cluster.run_clustering_model(new_rand_model=0, show_dend=0, show_shil=0, show_cluster_labels=0)
    print('\nCreando modelo predictivo..\n')
    Predict.run_selector(op=1)