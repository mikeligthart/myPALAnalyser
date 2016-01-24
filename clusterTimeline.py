import numpy as np
from sklearn.cluster import SpectralClustering

timeline_npy = 'data/cleaned/timeline.npy'
data = np.load(timeline_npy)

temp_flattened = []
for participant_index in range(0, len(data)):
    temp_flattened.append(data[0,:,:].flatten())
cluster_data = np.array(temp_flattened)

y_pred = SpectralClustering(n_clusters=3).fit_predict(cluster_data)
