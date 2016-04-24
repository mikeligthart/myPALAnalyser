# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 16:01:21 2016

@author: Mike
"""
import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Settings
debug = False
save_as = 'png'
number_of_days = 23

# Load data
login_time = np.load('data/cleaned/login_time.npy')
average_nr_of_words = np.load('data/cleaned/average_nr_of_words.npy')
personal_score = np.load('data/cleaned/personal_score.npy')
goal_difficulity = np.load('data/cleaned/goal_difficulty.npy')
median = np.load('data/cleaned/content_median.npy')
iqr = np.load('data/cleaned/content_iqr.npy')
total = np.load('data/cleaned/content_total.npy')

participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, number_of_days)]

def get_summary_text(median, iqr, total, median2 = None, iqr2 = None, total2 = None):
    median = round(median, 1)
    iqr = round(iqr, 1)
    total = round(total, 1)
    if median2 is None:
        if median >= 0:
            return 'median = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
        else:
            return 'No summary details\navailable'
    else:
        median2 = round(median2, 1)
        iqr2 = round(iqr2, 1)
        total2 = round(total2, 1)
        if median >= 0 and median2 >= -1:
            return '              D      T \nmedian: ' + str(median) + '    '+ str(median2) +'\nIQR:       '+ str(iqr) +'    ' + str(iqr2) + '\ntotal:     ' + str(total) + '  '+ str(total2)
        elif median >= 0 and median2 == -1:
            return 'Daily:\nmedian = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
        elif median == -1 and median2 >= 0:
            return 'Total:\nmedian = ' + str(median2) + '\nIQR = ' + str(iqr2) + '\nTotal = ' + str(total2)
        else:   
            return 'No summary details\navailable'

def set_y_lim(ax, y, y_lim, y_range, bars, bars2 = None):
    ax.set_yticks(range(y_lim + 1)[0::y_range])
    ax.set_yticklabels(range(y_lim + 1)[0::y_range], size=7)
    ax.set_ylim([0,y_lim])
    if not bars2:
        for index in np.where(y > y_lim)[0]:
            rect = bars[index]
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.8, '%d' % int(height), ha='center', va='bottom', size=5)
    else:
        for index in range(0, len(y)):
            rect1 = bars[index]
            rect2 = bars2[index]
            h1 = rect1.get_height()
            h2 = rect2.get_height()
            if (h1 + h2) > y_lim:
                ax.text(rect1.get_x() + rect1.get_width()/2., 0.5, 'd: %d' % int(h1), ha='center', va='bottom', size=5)
                ax.text(rect2.get_x() + rect2.get_width()/2., 10, 't: %d' % int(h2), ha='center', va='bottom', size=5)
    return ax

def get_y_color(y, y_lim):
    y_color = np.repeat(np.array(['b']), len(y))
    y_color[y > y_lim] = 'r'
    return y_color
        
# Build plots using matplotlib
bar_width = 0.35
font_prop = FontProperties()
font_prop.set_size('x-small')

#Red and blue line to indicate the evaluation session and the half way point    
stop_data=[21, 20, 14, 19, 20, 19, 24, 19, 20, 14, 20, 16, 21, 20]
half_way=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9]

#In debug mode only 1 timeline will be rendered
numberOfParticipants = len(participants)
if (debug):
    numberOfParticipants = 1

for participant_index in range(0, numberOfParticipants):
    ## GENERAL PLOT SETTINGS ##
    f, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True)
    x = get_list_of_dates(participants[participant_index]['start_date'])
    temp_x = [i for i in range(0, len(x))]
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=7)
    ttl = f.text(0.5, 1.01, 'Content timeline participant ' + str(participant_index+1), ha='center', size=16)
    dpifig = 300
    
    ## LOGIN TIME ##
    y = login_time[participant_index, 0:number_of_days]/60
    y_lim = 50    
    y_range = 10
    
    #plot
    bars = ax0.bar(temp_x, y, width=bar_width, color=get_y_color(y, y_lim))
    ax0 = set_y_lim(ax0, y, y_lim, y_range, bars)
    
    #labels and lines    
    ax0.set_title('Login time')
    y_lbl0 = ax0.set_ylabel("Minutes")
    ax0.axvline(stop_data[participant_index], color='r')
    ax0.axvline(half_way[participant_index], color='b')  

    #metrics
    metrics0 = f.text(1.005, 0.84, get_summary_text(median[participant_index, 0], iqr[participant_index, 0], total[participant_index, 0]), size=7)

    ## NUMBER OF WORDS ##
    y = average_nr_of_words[participant_index, 0:number_of_days] 
    y_lim = 25
    y_range = 5    
    
    #plot
    bars = ax1.bar(temp_x, y, width=bar_width, color=get_y_color(y, y_lim))
    ax1 = set_y_lim(ax1, y, y_lim, y_range, bars)

    #labels and lines     
    ax1.set_title('Average number of words')    
    y_lbl1 = ax1.set_ylabel("# words")
    ax1.axvline(stop_data[participant_index], color='r')
    ax1.axvline(half_way[participant_index], color='b')
    
    #Metrics
    metrics1 = f.text(1.005, 0.60, get_summary_text(median[participant_index, 1], iqr[participant_index, 1], total[participant_index, 1]), size=7)
    
    ## PERSONAL LEVEL ##
    y = personal_score[participant_index, 0:number_of_days]
    ax2.bar(temp_x, y, width=bar_width)
    ax2.set_title('Personal level of added content')
    y_lbl2 = ax2.set_ylabel("Personal level")
    y_ticks = [0, 1, 2, 3, 4]
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels(y_ticks, size=7)
    ax2.axvline(stop_data[participant_index], color='r')
    ax2.axvline(half_way[participant_index], color='b')
    metrics2 = f.text(1.005, 0.38, get_summary_text(median[participant_index, 2], iqr[participant_index, 2], total[participant_index, 2]), size=7)

    ## GOAL DIFFICULTY ##
    y_daily = goal_difficulity[participant_index, 0:number_of_days, 0]    
    y_total = goal_difficulity[participant_index, 0:number_of_days, 1]
    y_lim = 10
    y_range = 2
      
    #plot
    bars1 = ax3.bar(temp_x, y_daily, width=bar_width, color='b', label='Daily Goals')
    bars2 = ax3.bar(temp_x, y_total, width=bar_width, bottom=y_daily, color='c', label='Total Goals')
    #ax3.set_yticks(range(y_lim + 1)[0::y_range])
    #ax3.set_yticklabels(range(y_lim + 1)[0::y_range], size=7)
    #ax3.set_ylim([0,y_lim])
    ax3 = set_y_lim(ax3, y_daily, y_lim, y_range, bars1, bars2)
    
    #labels and lines
    ax3.set_title('Goal difficulty')
    y_lbl3 = ax3.set_ylabel("Difficulty")
    ax3.set_xlabel("Date")
    ax3.axvline(stop_data[participant_index], color='r')
    ax3.axvline(half_way[participant_index], color='b')
    
    #metrics and legend
    lgd3 = ax3.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.45, 1.25), title='Goals')
    metrics3 = f.text(1.005, 0.13, get_summary_text(median[participant_index, 3], iqr[participant_index, 3], total[participant_index, 3], median[participant_index, 4], iqr[participant_index, 4], total[participant_index, 4]), size=7)

    f.tight_layout()
    
    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(ttl, y_lbl0, y_lbl1, y_lbl2, y_lbl3, lgd3, metrics0, metrics1, metrics2, metrics3, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_timeline_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=(ttl, y_lbl0, y_lbl1, y_lbl2, y_lbl3, lgd3, metrics0, metrics1, metrics2, metrics3, ), bbox_inches='tight', format='svg')
    plt.close(f)

