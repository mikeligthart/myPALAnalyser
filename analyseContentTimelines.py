# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:26:24 2016

@author: Mike
"""
import numpy as np

# Load timelines numpy
login_time = np.load('data/cleaned/login_time.npy') / 60
average_nr_of_words = np.load('data/cleaned/average_nr_of_words.npy')
personal_score = np.load('data/cleaned/personal_score.npy')
goal_difficulity = np.load('data/cleaned/goal_difficulty.npy')

# General info
nr_of_participants = int(login_time.shape[0])
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
median = np.ones([nr_of_participants, 5]) * -1
iqr = np.ones([nr_of_participants, 5]) * -1
total = np.zeros([nr_of_participants, 5])

for index in range(0, nr_of_participants):
    #Calculate median    
    median[index, 0] = calc_median(login_time, index)
    median[index, 1] = calc_median(average_nr_of_words, index)
    median[index, 2] = calc_median(personal_score, index)
    median[index, 3] = calc_median(goal_difficulity[:,:,0], index)
    median[index, 4] = calc_median(goal_difficulity[:,:,1], index)
    
    #Calulate Interquarile range
    iqr[index, 0] = calc_iqr(login_time, index)
    iqr[index, 1] = calc_iqr(average_nr_of_words, index)
    iqr[index, 2] = calc_iqr(personal_score, index)
    iqr[index, 3] = calc_iqr(goal_difficulity[:,:,0], index)
    iqr[index, 4] = calc_iqr(goal_difficulity[:,:,1], index)
    
    #Calculate sum
    total[index, 0] = np.sum(login_time[index, :])
    total[index, 1] = np.sum(average_nr_of_words[index, :])
    total[index, 2] = np.sum(personal_score[index, :])
    total[index, 3] = np.sum(goal_difficulity[index,:,0])
    total[index, 4] = np.sum(goal_difficulity[index,:,1])

np.save('data/cleaned/content_median.npy', median)
np.save('data/cleaned/content_iqr.npy', iqr)
np.save('data/cleaned/content_total.npy', total)
