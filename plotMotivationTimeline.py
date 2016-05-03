# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 08:21:54 2016

@author: Mike Ligthart
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import statsmodels.stats.api as sms


#Seetings
with_plot = False
debug = False
save_as = 'png'

with open('data/cleaned/motivation.csv', 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    motivations = list(reader)

if debug:
    nr_of_participants = 1
else:
    nr_of_participants = len(motivations)


plot_headers = [['preMot', 'halfMot', 'postMot'],
                ['preAut', 'halfAut', 'postAut'],
                ['preCom', 'halfCom', 'postCom'],
                ['preRel', 'halfRel', 'postRel']]
nr_of_headers = len(plot_headers)
nr_of_measurements = len(plot_headers[0])

plot_index = [[0, 0], [0, 1], [1, 0], [1, 1]]

def get_subplot(axarr, header_index):
    if header_index == 0:
        subplot = axarr[0, 0]
        subplot.set_title('General motivation', size=7)
        return subplot
    elif header_index == 1:
        subplot = axarr[0, 1]
        subplot.set_title('Feeling of Autonomy', size=7)
        return subplot
    elif header_index == 2:
        subplot = axarr[1, 0]
        subplot.set_title('Feeling of Competence', size=7)
        return subplot
    elif header_index == 3:
        subplot = axarr[1, 1]
        subplot.set_title('Feeling of Reletedness', size=7)
        return subplot
    else:
        return None

total_motivation = np.zeros([nr_of_participants, nr_of_headers])
motivation_array = np.zeros([nr_of_headers, nr_of_participants, nr_of_measurements])
mean_motivation = np.zeros([nr_of_headers, nr_of_measurements])
confidence_interval = np.zeros([nr_of_headers, nr_of_measurements, 2])

for participant in range(0, nr_of_participants):
    if with_plot:
        f, axarr = plt.subplots(2,2)
        plot_title = 'Motivation timeline participant ' + str(participant+1)
        ttl = f.text(0.5, 1.01, plot_title, ha='center', size=16)
        x = np.array([1, 2, 3])
        dpifig = 300
    
    for header_index in range(0,nr_of_headers):
        y = []
        for header in plot_headers[header_index]:
            y.append(float(motivations[participant].get(header)))
        y = np.array(y)
        total_motivation[participant, header_index] = np.trapz(y)
        motivation_array[header_index, participant, :] = y
        #mean_motivation[participant, header_index] = np.mean(y)
        #confidence_interval[participant, header_index] = sms.DescrStatsW(y).tconfint_mean
        
        if with_plot:
            subplot = get_subplot(axarr, header_index)
            subplot.plot(x, y)
            subplot.set_xticks(x)
            subplot.set_xticklabels(plot_headers[header_index], size=7)
            subplot.set_ylim([1,7])
      
    if with_plot:
        f.tight_layout()
    
        if save_as == "png" or save_as == "both":
            plt.savefig('data/cleaned/timelines/motivation/motivation_timeline_p' + str(participant + 1) + '.png', bbox_extra_artists=(ttl, ), bbox_inches='tight', dpi=dpifig)
        if save_as == "svg" or save_as == "both":
            plt.savefig('data/cleaned/timelines/motivation/motivation_timeline_p' + str(participant + 1) + '.svg', bbox_extra_artists=(ttl, ), bbox_inches='tight', format='svg')
        plt.close(f)
        
for header_index in range(0, nr_of_headers):
    for measurement_index in range(0, nr_of_measurements):
        y = motivation_array[header_index, :, measurement_index]
        mean_motivation[header_index, measurement_index] = np.mean(y) 
        ci = sms.DescrStatsW(y).tconfint_mean()  
        confidence_interval[header_index, measurement_index, 0] = ci[0]
        confidence_interval[header_index, measurement_index, 1] = ci[1]

for measurement_index in range(0, nr_of_measurements):
    plt.errorbar(measurement_index, mean_motivation[0, measurement_index], yerr = list(confidence_interval[0, measurement_index, :]))

if not debug:
    np.save('data/cleaned/total_motivation.npy', total_motivation)


        
            