import csv
import os
from datetime import datetime
from operator import itemgetter
import re

activitiesCSV = 'data/raw/activities.csv'
activityTypeCSV = 'data/raw/activity_types.csv'
picturesCSV = 'data/raw/pictures.csv'
pictureFolder = 'data/raw/pictures/'
goalsCSV = 'data/raw/goals.csv'
personalLevelCSV='data/cleaned/personal_level.csv'

#Load base CSV files
rawActivities = []
activities = []
activityTypes = []
personal_level = []
pictures = []
rawGoals = []
goals = []

with open(activitiesCSV, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    rawActivities = list(reader)

with open(activityTypeCSV, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    activityTypes = list(reader)

with open(personalLevelCSV, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    personal_level = list(reader)

with open(picturesCSV, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    pictures = list(reader)
    
with open(goalsCSV, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    rawGoals = list(reader)

def isOnDelList(name):
    delList = ['mike.ligthart', 'hunter', 'elvira', 'viewer']
    return name in delList

def changeNameForNumber(name):
    numberForName = ['benja', 'sinne', 'daan', 'tom', 'rick', 'martijn', 'hunter', 'ilse', 'casper', 'safiye', 'yasmin', 'koen', 'maas', 'janwillem']
    return 1 + numberForName.index(name)

def findPicture(pictures, picture_id):
    for picture in pictures:
        if picture['ID'] == picture_id:
            return picture['NAME']
    return None

def findActivityType(activity_types, activity_type_id):
    for activity_type in activity_types:
        if activity_type['ID'] == activity_type_id:
            return activity_type['NAME'].lower()
    return None

# Process pictures
for index in range(0, len(pictures)):
    pictures[index]['USER_USER_NAME'] = changeNameForNumber(pictures[index]['USER_USER_NAME'])
    newName = str(pictures[index]['USER_USER_NAME']) + '_' + pictures[index]['ID'] + '.' + pictures[index]['NAME'].split('.')[1]
    #os.rename(pictureFolder + pictures[index]['NAME'], pictureFolder + newName)
    pictures[index]['NAME'] = newName
    pictures[index]['ADDED'] = datetime.strptime(pictures[index]['ADDED'].split('.')[0], '%Y-%m-%d %H:%M:%S')
    del pictures[index]['THUMBNAIL']
    del pictures[index]['DATE']

with open('data/cleaned/pictures.csv', 'wb') as outputFile:
    writer = csv.DictWriter(outputFile, pictures[0].keys())
    writer.writeheader()
    writer.writerows(pictures)

# Process activities
for rawActivity in rawActivities:
    activity = {}
    activity['participant'] = changeNameForNumber(rawActivity['USER_NAME'])
    activity['added'] = datetime.strptime(rawActivity['ADDED'].split('.')[0], '%Y-%m-%d %H:%M:%S')
    activity['start'] = datetime.strptime(rawActivity['DATE'] + ' ' + rawActivity['STARTTIME'], '%Y-%m-%d %H:%M:%S')
    activity['end'] = datetime.strptime(rawActivity['DATE'] + ' ' + rawActivity['STARTTIME'], '%Y-%m-%d %H:%M:%S')
    activity['type'] = findActivityType(activityTypes, rawActivity['TYPE_ID'])
    activity['name'] = rawActivity['NAME']
    activity['description'] = rawActivity['DESCRIPTION']
    activity['emotion'] = rawActivity['EMOTION']
    activity['picture'] = findPicture(pictures, rawActivity['PICTURE_ID'])
    activity['carbohydrate_value'] = rawActivity['CARBOHYDRATE_VALUE']
    activity['#words'] = len(re.findall(r'\w+', rawActivity['DESCRIPTION']))
    personal_dict = (act for act in personal_level if act["added"] == activity['added'].strftime("%Y-%m-%d %H:%M:%S")).next()
    activity['personal'] = personal_dict['personal']
    activities.append(activity)
    activities = sorted(activities, key=itemgetter('added'))

with open('data/cleaned/activities.csv', 'wb') as outputFile:
    writer = csv.DictWriter(outputFile, activities[0].keys())
    writer.writeheader()
    writer.writerows(activities)
   
# Process goals
    for rawGoal in rawGoals:
        if isOnDelList(rawGoal['USER_USER_NAME']) == False:
            goal = {}
            goal['participant'] = changeNameForNumber(rawGoal['USER_USER_NAME'])
            goal['added'] = datetime.strptime(rawGoal['ADDED'].split('.')[0], '%Y-%m-%d %H:%M:%S')
            goal['goal_type'] = rawGoal['GOAL_TYPE']
            goal['target'] = rawGoal['TARGET']
            goal['value'] = int(rawGoal['TARGET_VALUE'])
            goal['met'] = rawGoal['MET'] == "TRUE"
            goal['deadline'] = datetime.strptime(rawGoal['DEADLINE'].split('.')[0], '%Y-%m-%d %H:%M:%S')
            if(goal['met']):
                goal['met_at'] = datetime.strptime(rawGoal['MET_AT_TIMESTAMP'].split('.')[0], '%Y-%m-%d %H:%M:%S')
            else:
                goal['met_at'] = ''
            goals.append(goal)
            goals = sorted(goals, key=itemgetter('added'))
            
with open('data/cleaned/goals.csv', 'wb') as outputFile:
    writer = csv.DictWriter(outputFile, goals[0].keys())
    writer.writeheader()
    writer.writerows(goals)           