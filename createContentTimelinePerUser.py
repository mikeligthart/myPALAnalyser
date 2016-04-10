# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:05:09 2016

@author: Mike
"""

import numpy as np
import csv
from datetime import datetime, timedelta
from operator import itemgetter

#Parameters
nr_of_days = 24
session = 15 * 60

# Load participant CSV
participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)
    
user_logs_CSV = 'data/cleaned/user_logs.csv'
with open(user_logs_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    user_logs = list(reader)

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, nr_of_days)]   

def get_cummalative_login_time(logs, total_seconds):
    if len(logs) <= 1:
        return total_seconds
    else:
         time_difference = logs[1]['timestamp'] - logs[0]['timestamp']
         time_difference_seconds = time_difference.total_seconds()
         if (time_difference_seconds < session):
             total_seconds += time_difference_seconds
             del logs[0]
         else:
             del logs[0]
         
         return get_cummalative_login_time(logs, total_seconds)
        
    
def get_login_time(logs):
    if len(logs) > 1:
        sorted_logs = sorted(logs, key=itemgetter('timestamp'))
        time_difference = sorted_logs[-1]['timestamp'] - sorted_logs[0]['timestamp']
        total_seconds = time_difference.total_seconds()
        if total_seconds <= session:
            return total_seconds
        else:
            return get_cummalative_login_time(sorted_logs, 0)
    else:
        return 0
    
for log in user_logs:
    log['timestamp'] = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')    

login_time = np.zeros([len(participants), nr_of_days])  
for participant_index in range(0, len(participants)):
    logs_for_participant = filter(lambda log: log['participant'] == participants[participant_index]['participant'], user_logs)
    dates = get_list_of_dates(participants[participant_index]['start_date'])
    for date_index in range(0, nr_of_days):
        logs_for_participant_for_date = filter(lambda log: log['timestamp'].date() == dates[date_index], logs_for_participant)
        login_time[participant_index][date_index] = get_login_time(logs_for_participant_for_date)
        
np.save('data/cleaned/login_time.npy', login_time)