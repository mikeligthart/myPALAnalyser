# -*- coding: utf-8 -*-
"""
Created on Tue May 03 11:09:09 2016

@author: Mike
"""
import numpy as np
import matplotlib.pyplot as plt

#Settings
debug = False
save_as = 'png'

motivations = np.load('data/cleaned/motivation.npy')
total_motivation = np.load('data/cleaned/motivation_total.npy')
mean_motivation = np.load('data/cleaned/motivation_mean.npy')
confidence_interval= np.load('data/cleaned/motivation_ci.npy')

if debug:
    nr_of_participants = 1
else:
    nr_of_participants = len(motivations[0])

nr_of_headers = len(motivations)
nr_of_measurements = len(motivations[0][0])

x = [1, 2, 3]
y = mean_motivation[0, :]
yerr = [y - confidence_interval[0, :, 0], confidence_interval[0, :, 1] - y]

plt.errorbar(x, y, yerr = yerr)
plt.title('Mean motivation with 95% confidence intervals')

plt.xlabel('Time')
plt.xlim([0, 4])
plt.xticks(x, ['pre', 'half way', 'post'], size=8)

plt.ylabel('Motivation score')
plt.ylim([1, 7])

plt.grid()
plt.savefig('data/cleaned/summary_plots/mean_motivation_all.png', bbox_inches='tight', dpi=300)