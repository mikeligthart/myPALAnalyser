# -*- coding: utf-8 -*-
"""
Created on Tue May 03 10:43:40 2016

@author: Mike
"""

import numpy as np
import csv
import statsmodels.stats.api as sms

with open('data/cleaned/motivation.csv', 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    motivations = list(reader)

plot_headers = [['preMot', 'halfMot', 'postMot'],
                ['preAut', 'halfAut', 'postAut'],
                ['preCom', 'halfCom', 'postCom'],
                ['preRel', 'halfRel', 'postRel']]
  
nr_of_participants = len(motivations)              
nr_of_headers = len(plot_headers)
nr_of_measurements = len(plot_headers[0])

total_motivation = np.zeros([nr_of_participants, nr_of_headers])
motivation_array = np.zeros([nr_of_headers, nr_of_participants, nr_of_measurements])
mean_motivation = np.zeros([nr_of_headers, nr_of_measurements])
confidence_interval = np.zeros([nr_of_headers, nr_of_measurements, 2])

for participant in range(0, nr_of_participants):    
    for header_index in range(0,nr_of_headers):
        y = []
        for header in plot_headers[header_index]:
            y.append(float(motivations[participant].get(header)))
        y = np.array(y)
        total_motivation[participant, header_index] = np.trapz(y)
        motivation_array[header_index, participant, :] = y
               

for header_index in range(0, nr_of_headers):
    for measurement_index in range(0, nr_of_measurements):
        y = motivation_array[header_index, :, measurement_index]
        mean_motivation[header_index, measurement_index] = np.mean(y) 
        ci = sms.DescrStatsW(y).tconfint_mean()  
        confidence_interval[header_index, measurement_index, 0] = ci[0]
        confidence_interval[header_index, measurement_index, 1] = ci[1]

deg = 2
x = [1, 2, 3]
z = np.zeros([nr_of_participants, deg + 1])
for participant in range(0, nr_of_participants):
    y = motivation_array[0, participant, :]
    z[participant, :] = np.polyfit(x, y, deg)

np.save('data/cleaned/motivation.npy', motivation_array)
np.save('data/cleaned/motivation_total.npy', total_motivation)
np.save('data/cleaned/motivation_mean.npy', mean_motivation)
np.save('data/cleaned/motivation_ci.npy', confidence_interval)
np.save('data/cleaned/motivation_polyfit.npy', z)