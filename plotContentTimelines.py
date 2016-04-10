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

# Settings
debug = False
save_as = 'png'

# Load data
login_time = np.load('data/cleaned/login_time.npy')
average_nr_of_words = np.load('data/cleaned/average_nr_of_words.npy')

participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, 23)]

def get_yticks(y, nr_of_steps):
    max_y = int(math.ceil(np.max(y)))
    y_ticks = range(0, max_y)
    y_step_size = int(math.ceil(max_y / nr_of_steps))
    if(y_step_size < 1):
        y_step_size = 1
    else:
        y_step_size = int(math.ceil(y_step_size / 5.0)) * 5
    return y_ticks[0::y_step_size]

# Build plots using matplotlib
bar_width = 0.35

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
    y = login_time[participant_index, 0:23]/60
    ax0.bar(temp_x, y, width=bar_width)
    ax0.set_title('Login time')
    y_lbl0 = ax0.set_ylabel("Minutes")
    y_ticks = get_yticks(y, 4)
    ax0.set_yticks(y_ticks)
    ax0.set_yticklabels(y_ticks, size=7)

    #Number of words
    y = average_nr_of_words[participant_index, 0:23]
    ax1.bar(temp_x, y, width=bar_width)
    ax1.set_title('Average number of words')    
    y_lbl1 = ax1.set_ylabel("# words")
    y_ticks = get_yticks(y, 4)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_ticks, size=7)
    
    #Personal level
    ax2.bar(temp_x, np.zeros(23), width=bar_width)
    ax2.set_title('Personal level of activities')
    y_lbl2 = ax2.set_ylabel("Personal level")

    #Goal dificultiy
    ax3.bar(temp_x, np.zeros(23), width=bar_width)
    ax3.set_title('Goal difficulty')
    y_lbl3 = ax3.set_ylabel("Difficulty")
    ax3.set_xlabel("Date")

    f.tight_layout()
    
    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(ttl, y_lbl0, y_lbl1, y_lbl2, y_lbl3, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_timeline_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=(ttl, y_lbl0, y_lbl1, y_lbl2, y_lbl3, ), bbox_inches='tight', format='svg')
    plt.close(f)

