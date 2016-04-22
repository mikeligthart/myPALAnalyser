# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 16:01:21 2016

@author: Mike
"""
import numpy as np
import math
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

participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, number_of_days)]

def get_yticks(y, nr_of_steps):
    max_y = int(math.ceil(np.max(y)))
    y_ticks = range(0, max_y)
    y_step_size = int(math.ceil(max_y / nr_of_steps))
    if(y_step_size < 2):
        y_step_size = 1
    else:
        y_step_size = int(math.ceil(y_step_size / 5.0)) * 5
    return y_ticks[0::y_step_size]

# Build plots using matplotlib
bar_width = 0.35
font_prop = FontProperties()
font_prop.set_size('x-small')

#Red and blue line to indicate the evaluation session and the half way point    
stop_data=[21, 20, 14, 19, 20, 19, 24, 19, 20, 14, 20, 16, 21, 20]
half_way=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9]

numberOfParticipants = len(participants)
if (debug):
    numberOfParticipants = 1

for participant_index in range(0, numberOfParticipants):
    #General plot features
    f, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True)
    x = get_list_of_dates(participants[participant_index]['start_date'])
    temp_x = [i for i in range(0, len(x))]
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=7)
    ttl = f.text(0.5, 1.01, 'Content timeline participant ' + str(participant_index+1), ha='center', size=16)
    dpifig = 300
    
    #Login Time
    #Data processing
    y = login_time[participant_index, 0:number_of_days]/60
    y_nonzero = y[np.nonzero(y)]
    if len(y_nonzero) > 0:
        median = round(np.median(y_nonzero), 1)
        iqr = round(np.subtract(*np.percentile(y_nonzero, [75, 25])),1)   
        total = np.sum(y)
        text = 'median = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
    else:
        text = 'No summary details\navailable'
        
    #Plot processing
    ax0.bar(temp_x, y, width=bar_width)
    ax0.set_title('Login time')
    y_lbl0 = ax0.set_ylabel("Minutes")
    #y_ticks = get_yticks(y, 4)
    #ax0.set_yticks(y_ticks)
    #ax0.set_yticklabels(y_ticks, size=7)
    ax0.set_yticks(range(41)[0::10])
    ax0.set_yticklabels(range(41)[0::10], size=7)
    ax0.set_ylim([0,40])
    ax0.axvline(stop_data[participant_index], color='r')
    ax0.axvline(half_way[participant_index], color='b')
    metrics0 = f.text(1.005, 0.84, text, size=7)

    #Number of words
    y = average_nr_of_words[participant_index, 0:number_of_days]
    y_nonzero = y[np.nonzero(y)]
    if len(y_nonzero) > 0:
        median = np.median(y_nonzero)
        iqr = np.subtract(*np.percentile(y_nonzero, [75, 25]))    
        total = np.sum(y)
        text = 'median = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
    else:
        text = 'No summary details\navailable'
    
    ax1.bar(temp_x, y, width=bar_width)
    ax1.set_title('Average number of words')    
    y_lbl1 = ax1.set_ylabel("# words")
    y_ticks = get_yticks(y, 4)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_ticks, size=7)
    ax1.axvline(stop_data[participant_index], color='r')
    ax1.axvline(half_way[participant_index], color='b')
    metrics1 = f.text(1.005, 0.60, text, size=7)
    
    #Personal level
    y = personal_score[participant_index, 0:number_of_days]
    y_nonzero = y[np.nonzero(y)]
    if len(y_nonzero) > 0:
        median = round(np.median(y_nonzero),1)
        iqr = round(np.subtract(*np.percentile(y_nonzero, [75, 25])),1)  
        total = np.sum(y)
        text = 'median = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
    else:
        text = 'No summary details\navailable'
        
    ax2.bar(temp_x, y, width=bar_width)
    ax2.set_title('Personal level of added content')
    y_lbl2 = ax2.set_ylabel("Personal level")
    y_ticks = [0, 1, 2, 3, 4]
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels(y_ticks, size=7)
    ax2.axvline(stop_data[participant_index], color='r')
    ax2.axvline(half_way[participant_index], color='b')
    metrics2 = f.text(1.005, 0.38, text, size=7)

    #Goal dificultiy
    y_daily = goal_difficulity[participant_index, 0:number_of_days, 0]
    y_daily_nonzero = y_daily[np.nonzero(y_daily)]
    if len(y_daily_nonzero) > 0:
        median_daily = round(np.median(y_daily_nonzero),1)
        iqr_daily = round(np.subtract(*np.percentile(y_daily_nonzero, [75, 25])),1)   
        total_daily = np.sum(y_daily)
    
    y_total = goal_difficulity[participant_index, 0:number_of_days, 1]
    y_total_nonzero = y_total[np.nonzero(y_total)]
    if len(y_total_nonzero) > 0:
        median_total = round(np.median(y_total_nonzero),1)
        iqr_total = round(np.subtract(*np.percentile(y_total_nonzero, [75, 25])),1)
        total_total = np.sum(y_total)

    if len(y_daily_nonzero) > 0 and len(y_total_nonzero) > 0:
        text = '              D      T \nmedian: ' + str(median_daily) + '    '+ str(median_total) +'\nIQR:       '+ str(iqr_daily) +'    ' + str(iqr_total) + '\ntotal:     ' + str(total_daily) + '  '+ str(total_total)
    elif len(y_daily_nonzero) > 0 and len(y_total_nonzero) == 0:
        text = 'Daily:\nmedian = ' + str(median_daily) + '\nIQR = ' + str(iqr_daily) + '\nTotal = ' + str(total_daily)
    elif len(y_daily_nonzero) == 0 and len(y_total_nonzero) > 0:
        text = 'Total:\nmedian = ' + str(median_total) + '\nIQR = ' + str(iqr_total) + '\nTotal = ' + str(total_total)
    else:   
        text = 'No summary details\navailable'
        
    y_sum = np.sum(goal_difficulity[participant_index, 0:number_of_days, :], axis=1)
    ax3.bar(temp_x, y_daily, width=bar_width, color='b', label='Daily Goals')
    ax3.bar(temp_x, y_total, width=bar_width, bottom=y_daily, color='r', label='Total Goals')
    ax3.set_title('Goal difficulty')
    y_lbl3 = ax3.set_ylabel("Difficulty")
    ax3.set_xlabel("Date")
    y_ticks = get_yticks(y_sum, 4)
    ax3.set_yticks(y_ticks)
    ax3.set_yticklabels(y_ticks, size=7)
    ax3.axvline(stop_data[participant_index], color='r')
    ax3.axvline(half_way[participant_index], color='b')
    lgd3 = ax3.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.45, 1.25), title='Goals')
    metrics3 = f.text(1.005, 0.13, text, size=7)

    f.tight_layout()
    
    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(ttl, y_lbl0, y_lbl1, y_lbl2, y_lbl3, lgd3, metrics0, metrics1, metrics2, metrics3, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_timeline_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=(ttl, y_lbl0, y_lbl1, y_lbl2, y_lbl3, lgd3, metrics0, metrics1, metrics2, metrics3, ), bbox_inches='tight', format='svg')
    plt.close(f)

