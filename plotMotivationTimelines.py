# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 08:21:54 2016

@author: Mike Ligthart
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
z = np.load('data/cleaned/motivation_polyfit.npy')

if debug:
    nr_of_participants = 1
else:
    nr_of_participants = len(motivations[0])

nr_of_headers = len(motivations)
nr_of_measurements = len(motivations[0][0])

plot_index = [[0, 0], [0, 1], [1, 0], [1, 1]]

def get_subplot(axarr, header_index):
    if header_index == 0:
        subplot = axarr[0, 0]
        subplot.set_title('General motivation', size=9)
        subplot.set_ylabel('score', size=7)
        return subplot
    elif header_index == 1:
        subplot = axarr[0, 1]
        subplot.set_title('Feeling of Autonomy', size=9)
        subplot.set_ylabel('score', size=7)
        return subplot
    elif header_index == 2:
        subplot = axarr[1, 0]
        subplot.set_title('Feeling of Competence', size=9)
        subplot.set_ylabel('score', size=7)
        return subplot
    elif header_index == 3:
        subplot = axarr[1, 1]
        subplot.set_title('Feeling of Reletedness', size=9)
        subplot.set_ylabel('score', size=7)
        return subplot
    else:
        return None

plot_headers = [['preMot', 'halfMot', 'postMot'],
                ['preAut', 'halfAut', 'postAut'],
                ['preCom', 'halfCom', 'postCom'],
                ['preRel', 'halfRel', 'postRel']]

for participant in range(0, nr_of_participants):
    f, axarr = plt.subplots(2,2)
    plot_title = 'Motivation timeline participant ' + str(participant+1)
    ttl = f.text(0.5, 1.01, plot_title, ha='center', size=16)
    x = [1, 2, 3]
    dpifig = 300
    
    for header_index in range(0,nr_of_headers):
        y = motivations[header_index, participant, :]
        subplot = get_subplot(axarr, header_index)
        subplot.plot(x, y)
        subplot.set_xticks(x)
        subplot.set_xticklabels(plot_headers[header_index], size=7)
        subplot.set_ylim([1,7])
      
    f.tight_layout()

    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/motivation/motivation_timeline_p' + str(participant + 1) + '.png', bbox_extra_artists=(ttl, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/motivation/motivation_timeline_p' + str(participant + 1) + '.svg', bbox_extra_artists=(ttl, ), bbox_inches='tight', format='svg')
    plt.close(f)


        
            