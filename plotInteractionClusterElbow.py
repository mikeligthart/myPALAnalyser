# -*- coding: utf-8 -*-
"""
Created on Tue May 03 11:05:31 2016

@author: Mike
"""

#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

addedContent = np.load('data/cleaned/timeline_analysis_added_content.npy')
consistency = np.load('data/cleaned/timeline_analysis_consistency.npy')
consistency = 1/consistency
consistency[6] = 0

nr_of_clusters = [2, 3, 4, 5, 6, 7, 8, 9]
X = np.column_stack((consistency, addedContent))
X = np.delete(X, 6, 0)

score = []
for nr in nr_of_clusters:
    km = KMeans(n_clusters=nr)
    km.fit(X)
    score.append(km.score(X))

plt.plot(nr_of_clusters, score)
plt.plot(4, score[2], 'r.', markersize=8.0)
plt.plot(3, score[1], 'g.', markersize=8.0)
title = plt.title('Finding k for K-Means clustering: Elbow method', y=1.08)
x_label = plt.xlabel('Number of clusters')
y_label = plt.ylabel('Sum of distances to cluster center (score)')

plt.grid()
plt.savefig('data/cleaned/summary_plots/interaction_cluster_elbow.png', dpi=300, bbox_extra_artists=(title, x_label, y_label, ), bbox_inches='tight')
plt.close()