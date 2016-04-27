# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 08:21:54 2016

@author: Mike Ligthart
"""
import numpy as np
import matplotlib.pyplot as plt
import csv

#Seetings
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

total_motivation = np.zeros([nr_of_participants, 4])

for participant in range(0, nr_of_participants):
    f, axarr = plt.subplots(2,2)
    plot_title = 'Motivation timeline participant ' + str(participant+1)
    ttl = f.text(0.5, 1.01, plot_title, ha='center', size=16)
    x = np.array([1, 2, 3])
    dpifig = 300
    
    for header_index in range(0,len(plot_headers)):
        y = []
        for header in plot_headers[header_index]:
            y.append(float(motivations[participant].get(header)))
        y = np.array(y)
        total_motivation[participant, header_index] = np.trapz(y)
        
        subplot = get_subplot(axarr, header_index)
        subplot.plot(x, y)
        subplot.set_xticks(x)
        subplot.set_xticklabels(plot_headers[header_index], size=7)
    
    f.tight_layout()
    
    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/motivation/motivation_timeline_p' + str(participant + 1) + '.png', bbox_extra_artists=(ttl, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/motivation/motivation_timeline_p' + str(participant + 1) + '.svg', bbox_extra_artists=(ttl, ), bbox_inches='tight', format='svg')
    plt.close(f)

if not debug:
    np.save('data/cleaned/total_motivation.npy', total_motivation)


        
            