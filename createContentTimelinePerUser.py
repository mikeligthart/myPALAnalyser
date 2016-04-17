# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:05:09 2016

@author: Mike
"""

import numpy as np
import csv
from datetime import datetime, timedelta
from operator import itemgetter
import re

#Parameters
nr_of_days = 24
session = 15 * 60

# Load CSV info
participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)
    
user_logs_CSV = 'data/cleaned/user_logs.csv'
with open(user_logs_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    user_logs = list(reader)
    
activities_CSV = 'data/cleaned/activities.csv'
with open(activities_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    activities = list(reader)

goal_CSV = 'data/cleaned/goals.csv'
with open(goal_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    goals = list(reader)

#Transform data
for log in user_logs:
    log['timestamp'] = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')

for act in activities:
    act['added'] = datetime.strptime(act['added'], '%Y-%m-%d %H:%M:%S')
    
for goal in goals:
    goal['added'] = datetime.strptime(goal['added'], '%Y-%m-%d %H:%M:%S')
    goal['value'] = int(goal['value'])
    goal['met'] = goal['met'] == "TRUE"
    if goal['met']:
        goal['met_at'] = datetime.strptime(goal['met_at'], '%Y-%m-%d %H:%M:%S') 
    goal['deadline'] = goal['added'] + timedelta(days=goal['value'])

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

def get_average_nr_of_words(activities):
    if len(activities) > 0:
        nr_of_words = []
        for act in activities:
            nr_of_words.append(len(re.findall(r'\w+', act['description'])))
        return np.average(nr_of_words)
    else:
        return 0

def get_average_personal_score(activities):
    if len(activities) > 0:
        personal_score = []
        for act in activities:
            personal_score.append(int(act['personal']))
        return np.average(personal_score)
    else:
        return 0

def get_daily_goal_difficulty(goals):
    daily_score = 0
    for goal in goals:
        daily_score += goal['value']
    return daily_score

def get_total_goal_difficulty(goals, date):
    total_score = 0
    for goal in goals:
        day_delta = date - goal['added'].date()
        total_score += (goal['value'] - day_delta.days)
    return total_score

def is_relevant_goal(goal, date):
    if goal['goal_type'] == 'TOTAL' and goal['added'].date() <= date:
        if goal['met']:
            if goal['met_at'].date() < date:
                return True
        else:              
            if goal['deadline'].date() > date:
                return True
    return False

#Calculate content metrics per user per date  
login_time = np.zeros([len(participants), nr_of_days])
nr_of_words = np.zeros([len(participants), nr_of_days]) 
personal_score = np.zeros([len(participants), nr_of_days])
goal_difficulity = np.zeros([len(participants), nr_of_days, 2])

for participant_index in range(0, len(participants)):
    logs_for_participant = filter(lambda log: log['participant'] == participants[participant_index]['participant'], user_logs)
    activities_for_participant = filter(lambda act: act['participant'] == participants[participant_index]['participant'], activities)
    goals_for_participant = filter(lambda goal: goal['participant'] == participants[participant_index]['participant'], goals)    
    dates = get_list_of_dates(participants[participant_index]['start_date'])
    for date_index in range(0, nr_of_days):
        date = dates[date_index]
        logs_for_participant_for_date = filter(lambda log: log['timestamp'].date() == date, logs_for_participant)
        activities_for_participant_for_date = filter(lambda act: act['added'].date() == date, activities_for_participant)
        daily_goals_for_participant_for_date = filter(lambda goal: goal['added'].date() == date and goal['goal_type'] == 'DAILY', goals_for_participant)
        total_goals_for_participant_for_date = filter(lambda goal: is_relevant_goal(goal, date), goals_for_participant)
        
        # calculate content timeline values        
        login_time[participant_index][date_index] = get_login_time(logs_for_participant_for_date)
        nr_of_words[participant_index][date_index] = get_average_nr_of_words(activities_for_participant_for_date)
        personal_score[participant_index][date_index] = get_average_personal_score(activities_for_participant_for_date)        
        goal_difficulity[participant_index][date_index][0] = get_daily_goal_difficulty(daily_goals_for_participant_for_date)       
        goal_difficulity[participant_index][date_index][1] = get_total_goal_difficulty(total_goals_for_participant_for_date, date)        
        
np.save('data/cleaned/login_time.npy', login_time)
np.save('data/cleaned/average_nr_of_words.npy', nr_of_words)
np.save('data/cleaned/personal_score.npy', personal_score)
np.save('data/cleaned/goal_difficulty.npy', goal_difficulity)