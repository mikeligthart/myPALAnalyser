# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:31:00 2016

@author: Mike
"""
import csv
from datetime import datetime

#CSV source
avatar_logs_csv = 'data/raw/avatar_logs.csv'

raw_avatar_log_type = ['GREETING', 'COMPLIMENTED_MET_GOAL', 'ENCOURAGE_ACTIVE_GOAL', 'ENCOURAGE_ADDING_GOAL', 'REACT_HAPPY_SCHOOL',
                       'REACT_NEUTRAL_SCHOOL', 'REACT_SAD_SCHOOL', 'REACT_HAPPY_SPORT', 'REACT_NEUTRAL_SPORT', 'REACT_SAD_SPORT', 
                       'REACT_HAPPY_MEAL', 'REACT_NEUTRAL_MEAL', 'REACT_SAD_MEAL', 'REACT_HAPPY_OTHER', 'REACT_NEUTRAL_OTHER', 
                       'REACT_SAD_OTHER', 'ASK_TOGETHER_OR_SELF', 'ADDACTIVITYTOGETHER', 'REACT_GOAL_MET_AFTER', 'REACT_GOAL_ADDED',
                       'REACT_GOAL_ACTIVE', 'REACT_GOAL_NOT_ACTIVE']
                       
with open(avatar_logs_csv, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    raw_avatar_logs = list(reader)

def isOnDelList(name):
    delList = ['mike.ligthart', 'hunter', 'elvira', 'viewer']
    return name in delList

def changeNameForNumber(name):
    numberForName = ['benja', 'sinne', 'daan', 'tom', 'rick', 'martijn', 'hunter', 'ilse', 'casper', 'safiye', 'yasmin', 'koen', 'maas', 'janwillem']
    return 1 + numberForName.index(name)

avatar_logs = []

for raw_avatar_log in raw_avatar_logs:
    if isOnDelList(raw_avatar_log['USER_USER_NAME']) == False:
        avatar_log = {}
        avatar_log['participant'] = changeNameForNumber(raw_avatar_log['USER_USER_NAME'])
        avatar_log['timestamp'] = datetime.strptime(raw_avatar_log['TIMESTAMP'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        avatar_log['behavior'] = raw_avatar_log_type[int(raw_avatar_log['TYPE'])]
        avatar_logs.append(avatar_log)

with open('data/cleaned/avatar_logs.csv', 'wb') as outputFile:
    writer = csv.DictWriter(outputFile, avatar_logs[0].keys())
    writer.writeheader()
    writer.writerows(avatar_logs)
