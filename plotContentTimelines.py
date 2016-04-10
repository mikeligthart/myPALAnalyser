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
save_as = 'both'

# Load data
login_time = np.load('data/cleaned/login_time.npy')

participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, 23)]

# Build plots using matplotlib
bar_width = 0.8
font_prop = FontProperties()
font_prop.set_size('small')

numberOfParticipants = len(participants)
if (debug):
    numberOfParticipants = 1

for participant_index in range(0, numberOfParticipants):
    x = get_list_of_dates(participants[participant_index]['start_date'])
    y = login_time[participant_index, 0:23] / 60
    temp_x = [i for i in range(0, len(x))]
    plt.bar(temp_x, y, width=bar_width) 
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=8)
    
    y_label = plt.ylabel('Login time (minutes)')
    x_label = plt.xlabel('Date')
    title = plt.title('Content timeline participant ' + str(participant_index+1))
    dpifig = 300
       
    plt.tight_layout()
    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(y_label, title, x_label, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/content/content_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=(y_label, title, x_label, ), bbox_inches='tight', format='svg')
    plt.close()
