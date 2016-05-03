# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:42:28 2016

@author: Mike
"""

import numpy as np
import csv
from datetime import datetime, timedelta

#Parameters
nr_of_days = 23

# Load CSV info
avatar_logs_CSV = 'data/cleaned/avatar_logs.csv'
with open(avatar_logs_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    avatar_logs = list(reader)

participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)
nr_or_participants = len(participants)

#Transform data
for log in avatar_logs:
    log['timestamp'] = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, nr_of_days)]
    
avatar_interaction = np.zeros([nr_or_participants, nr_of_days])
for participant_index in range(0, nr_or_participants):
    avatar_logs_for_participant = filter(lambda log: log['participant'] == participants[participant_index]['participant'], avatar_logs)
    dates = get_list_of_dates(participants[participant_index]['start_date'])
    for date_index in range(0, len(dates)):
        avatar_logs_for_participant_for_date = filter(lambda log: log['timestamp'].date() == dates[date_index], avatar_logs_for_participant)                     
        avatar_interaction[participant_index, date_index] = len(avatar_logs_for_participant_for_date)  
        
np.save('data/cleaned/avatar_interaction.npy', avatar_interaction)