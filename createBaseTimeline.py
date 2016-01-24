import csv
from datetime import datetime

#CSV source
user_logs_csv = 'data/raw/user_logs.csv'

# for transfering the type ID to text
log_action_type = ['LOGIN', 'LOGOFF', 'ACCESSCALENDAR', 'ACCESSGOALS', 'ACCESSADDACTIVITYPAGE', 'ADDEDACTIVITY', 'ACCESSGALLERY', 'ACCESSADDPICTUREPAGE',
    'VIEWACTIVITY', 'DELETEACTIVITY', 'DELETEPICTUREFROMACTIVITY', 'UNLINKPICTUREFROMACTIVITY', 'UPDATEACTIVITY',
    'DELETEPICTUREFROMGALLERY', 'SELECTPICTUREFROMGALLRERYPAGE', 'ACCESSADDPICTUREDIRECTLYPAGE', 'ADDEDPICTUREDIRECTLY',
    'LINKPICTURETOACTIVITY', 'UPDATECALENDARDOWN', 'UPDATECALENDARUP', 'UPDATECALENDARDIRECTLY', 'ACCESSSELECTMEASUREMENTPAGE',
    'ACCESSADDGLUCOSEPAGE', 'ADDEDGLUCOSE', 'VIEWMEASUREMENT', 'ADDEDPICTURE', 'REMOVEDMEASUREMENT', 'UPDATEGLUCOSE', 'UPDATEINSULIN',
    'UPDATEDGLUCOSE', 'UPDATEDINSULINE', 'UPDATEDCARBOHYDRATE', 'UPDATECARBOHYDRATE', 'ACCESSADDCARBOHYDRATEPAGE', 'ADDEDINSULIN',
    'ADDEDCARBOHYDRATE', 'UPLOADEDPICTURE', 'ACCESSGOALADDDAILYPAGE', 'ADDEDGOALDAILY', 'ACCESSGOALADDTOTALPAGE', 'ADDEDGOALTOTAL',
    'DELETEGOAL', 'ACCESSUPDATEACTIVITYPAGE', 'ACCESSADDACTIVITYTYPEPAGE', 'ACCESSADDINSULINPAGE', 'ACCESSUPDATEGLUCOSEPAGE',
    'ACCESSUPDATEINSULINPAGE', 'ADDEDACTIVITYTYPE', 'DELETEACTIVITYTYPE', 'DELETEGLUCOSE', 'DELETEINSULIN', 'ADDEDWITHGLUCONLINE',
    'TOGETHERORSELF', 'TOGETHER']

with open(user_logs_csv, 'rb') as csvFile:
    reader = csv.DictReader(csvFile)
    raw_user_logs = list(reader)

def isOnDelList(name):
    delList = ['mike.ligthart', 'hunter', 'elvira', 'viewer']
    return name in delList

def changeNameForNumber(name):
    numberForName = ['benja', 'sinne', 'daan', 'tom', 'rick', 'martijn', 'hunter', 'ilse', 'casper', 'safiye', 'yasmin', 'koen', 'maas', 'janwillem']
    return 1 + numberForName.index(name)

user_logs = []

for raw_user_log in raw_user_logs:
    if isOnDelList(raw_user_log['USER_USER_NAME']) == False:
        user_log = {}
        user_log['participant'] = changeNameForNumber(raw_user_log['USER_USER_NAME'])
        user_log['timestamp'] = datetime.strptime(raw_user_log['TIMESTAMP'].split('.')[0], '%Y-%m-%d %H:%M:%S')
        user_log['behavior'] = log_action_type[int(raw_user_log['TYPE'])]
        user_logs.append(user_log)

with open('data/cleaned/user_logs.csv', 'wb') as outputFile:
    writer = csv.DictWriter(outputFile, user_logs[0].keys())
    writer.writeheader()
    writer.writerows(user_logs)
