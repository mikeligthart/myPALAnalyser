# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 13:06:24 2016

@author: Mike
"""

import numpy as np

# Load timelines numpy
avatar_interaction = np.load('data/cleaned/avatar_interaction.npy')

# General info
nr_of_participants = int(avatar_interaction.shape[0])
nr_of_active_days = [21, 20, 14, 19, 20, 19, 24, 19, 20, 14, 20, 16, 21, 20]

def calc_median(y, index):
    nonzero_y = y[index, y[index, :].nonzero()]
    if nonzero_y.size > 0:
        return np.median(nonzero_y)
    else:
        return -1

def calc_iqr(y, index):
    nonzero_y = y[index, y[index, :].nonzero()]
    if nonzero_y.size > 0:
        return np.subtract(*np.percentile(nonzero_y, [75, 25]))
    else:
        return -1

#Calculate median and IQR
median = np.ones([nr_of_participants]) * -1
iqr = np.ones([nr_of_participants]) * -1
total = np.zeros([nr_of_participants])

for index in range(0, nr_of_participants):
    #Calculate median    
    median[index] = calc_median(avatar_interaction, index)
   
    #Calulate Interquarile range
    iqr[index] = calc_iqr(avatar_interaction, index)
    
    #Calculate sum
    total[index] = np.sum(avatar_interaction[index, :])


np.save('data/cleaned/avatar_median.npy', median)
np.save('data/cleaned/avatar_iqr.npy', iqr)
np.save('data/cleaned/avatar_total.npy', total)
