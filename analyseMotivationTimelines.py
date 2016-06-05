# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 08:29:32 2016

@author: Mike Ligthart
"""
import numpy as np
import statsmodels.stats.api as sms
import matplotlib.pyplot as plt


#Define segments
segments = [[0, 4, 8 , 10], [2, 9, 11, 12, 13], [3, 5, 7]]

#Load data
motivation_index = 0
motivations = np.load('data/cleaned/motivation.npy')

#Plot
x = [1, 2, 3]
count = 0
for segment in segments:
    count += 1
    y = []
    ci1 = []
    ci2 = []
    yerr = []
    for measurement_index in range(0, 3):
        segment_score = motivations[motivation_index, segment, measurement_index]
        mean_segment_score = np.mean(segment_score)      
        y.append(mean_segment_score)
        ci = sms.DescrStatsW(segment_score).tconfint_mean()
        ci1.append(mean_segment_score - ci[0])
        ci2.append(ci[1] - mean_segment_score)
    
    yerr = [ci1, ci2]
    plt.errorbar(x, y, yerr = yerr)
    plt.title('Segment ' + str(count) + ': mean motivation with 95% confidence intervals')
    
    plt.xlabel('Time')
    plt.xlim([0, 4])
    plt.xticks(x, ['pre', 'half way', 'post'], size=8)
    
    plt.ylabel('Motivation score')
    plt.ylim([1, 7])
    
    plt.grid()
    plt.savefig('data/cleaned/summary_plots/mean_motivation_segment_' + str(count) + '.png', bbox_inches='tight', dpi=300)
    plt.clf()

plt.plot(x, motivations[motivation_index, 1, :])
plt.title("Motivation of participant 2")
plt.xlabel('Time')
plt.xlim([0, 4])
plt.xticks(x, ['pre', 'half way', 'post'], size=8)
plt.ylabel('Motivation score')
plt.ylim([1, 7])
plt.grid()
plt.savefig('data/cleaned/summary_plots/motivation_outlier_p2.png', bbox_inches='tight', dpi=300)