# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:46:24 2016

@author: Mike Ligthart
"""
import numpy as np
import matplotlib.pyplot as plt

added_content = np.load('data/cleaned/timeline_analysis_added_content.npy')
total_motivation = np.load('data/cleaned/total_motivation.npy')
consistency = np.load('data/cleaned/timeline_analysis_consistency.npy')

colors = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
"#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43"]
area=np.ones(14)*150
area[6]=5

for index in range(0,len(added_content)):
    label = 'p' + str(index+1)
    scatter_plot = plt.scatter(total_motivation[index,0], added_content[index], s=area[index], color=colors[index], alpha=0.5, label=label)    
    
plt.ylim([0,80])
plt.xlim([6, 12])
lgd = plt.legend(loc=0, scatterpoints = 1, bbox_to_anchor=(1.3, 1.08))
title = plt.title('Motivation versus Added content', y=1.08)
x_label = plt.xlabel('AUC Motivation')
y_label = plt.ylabel('#Added Content')

plt.grid()
plt.savefig('data/cleaned/summary_plots/motivation_vs_added_content.png', dpi=300, bbox_extra_artists=(lgd, title, x_label, y_label, ), bbox_inches='tight')
plt.close()

for index in range(0,len(consistency)):
    label = 'p' + str(index+1)
    scatter_plot = plt.scatter(total_motivation[index,0], 1/consistency[index], s=area[index], color=colors[index], alpha=0.5, label=label)    
    
plt.ylim([0,1])
plt.xlim([6, 12])
lgd = plt.legend(loc=0, scatterpoints = 1, bbox_to_anchor=(1.3, 1.08))
title = plt.title('Motivation versus Consistency', y=1.08)
x_label = plt.xlabel('AUC Motivation')
y_label = plt.ylabel('Consistency')

plt.grid()
plt.savefig('data/cleaned/summary_plots/motivation_vs_consistency.png', dpi=300, bbox_extra_artists=(lgd, title, x_label, y_label, ), bbox_inches='tight')
plt.close()