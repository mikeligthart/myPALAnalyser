# -*- coding: utf-8 -*-
"""
Created on Tue May 03 11:05:31 2016

@author: Mike
"""

#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

addedContent = np.load('data/cleaned/timeline_analysis_added_content.npy')
consistency = np.load('data/cleaned/timeline_analysis_consistency.npy')
consistency = 1/consistency
consistency[6] = 0

# Gaussian KDE
N = 14
X = addedContent * consistency
X = np.delete(X, 6, 0)
X = X[:, np.newaxis]
X_plot = np.linspace(0, 40, 1000)[:, np.newaxis]


kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(X)
log_dens = kde.score_samples(X_plot)
val = 0.004
plt.plot(X, np.zeros_like(X) + val, 'x')
plt.plot(X_plot[:, 0], np.exp(log_dens))