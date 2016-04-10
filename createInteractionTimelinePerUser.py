import csv
from datetime import datetime, timedelta
import numpy as np

# File paths
participants_CSV = 'data/cleaned/participants.csv'
user_logs_CSV = 'data/cleaned/user_logs.csv'

def get_timeline_filepath(feature_name):
    return 'data/cleaned/' + feature_name + '.npy'

# Global variables
participants = []
user_logs = []

date_range = range(0, 23)
time_x_axis = []
data_y_axis = []

feature_names = ['activity_timeline', 'measurement_timeline', 'picture_timeline', 'goal_timeline']
features = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'UPDATEACTIVITY', 'DELETEACTIVITY', 'ADDEDACTIVITYTYPE', 'DELETEACTIVITYTYPE', 'LOGOFF'],
            ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'REMOVEDMEASUREMENT', 'UPDATEGLUCOSE', 'UPDATEINSULIN', 'DELETEGLUCOSE', 'DELETEINSULIN', 'LOGOFF'],
            ['LOGIN', 'ACCESSGALLERY', 'ACCESSADDPICTUREPAGE', 'ACCESSADDPICTUREDIRECTLYPAGE','SELECTPICTUREFROMGALLRERYPAGE', 'ADDEDPICTUREDIRECTLY' 'ADDEDPICTURE', 'UPLOADEDPICTURE', 'LINKPICTURETOACTIVITY', 'DELETEPICTUREFROMACTIVITY', 'UNLINKPICTUREFROMACTIVITY', 'DELETEPICTUREFROMGALLERY', 'LOGOFF'],
            ['LOGIN', 'ACCESSGOALS','ACCESSGOALADDDAILYPAGE', 'ADDEDGOALDAILY', 'ACCESSGOALADDTOTALPAGE','ADDEDGOALTOTAL', 'DELETEGOAL', 'LOGOFF']]

# Load CSV files
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)

with open(user_logs_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    user_logs = list(reader)


## Generate Timeline Data ##
# Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in date_range]

def get_date_index(x_axis, date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()
    return x_axis.index(date)

# Main function
for feature_name_index in range(0, len(feature_names)):    
    # Prepare axis
    for participant in participants:
        time_x_axis.append(get_list_of_dates(participant['start_date']))
    data_y_axis = np.zeros([len(participants), len(date_range), len(features[feature_name_index])]) 

    # Retrieve data for data_y_axis
    for user_log in user_logs:
        for feature_index in range(0, len(features[feature_name_index])):
            if user_log['behavior'] == features[feature_name_index][feature_index]:
                participant_index = int(user_log['participant'])-1
                date_index = get_date_index(time_x_axis[participant_index], user_log['timestamp'])
                data_y_axis[participant_index][date_index][feature_index] += 1
    np.save(get_timeline_filepath(feature_names[feature_name_index]), data_y_axis)

