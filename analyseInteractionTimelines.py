import numpy as np
import csv
#from sklearn.cluster import SpectralClustering

# Load participant CSV
participants_CSV = 'data/cleaned/participants.csv'
with open(participants_CSV, 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    participants = list(reader)

# Load timelines numpy
activity_timeline = np.load('data/cleaned/activity_timeline.npy')
measurement_timeline = np.load('data/cleaned/measurement_timeline.npy')
picture_timeline = np.load('data/cleaned/picture_timeline.npy')
goal_timeline = np.load('data/cleaned/goal_timeline.npy')

# Names
feature_names = ['activity_timeline', 'measurement_timeline', 'picture_timeline', 'goal_timeline']
features = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'UPDATEACTIVITY', 'DELETEACTIVITY', 'ADDEDACTIVITYTYPE', 'DELETEACTIVITYTYPE', 'LOGOFF'], ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'REMOVEDMEASUREMENT', 'UPDATEGLUCOSE', 'UPDATEINSULIN', 'DELETEGLUCOSE', 'DELETEINSULIN', 'LOGOFF'], ['LOGIN', 'ACCESSGALLERY', 'ACCESSADDPICTUREPAGE', 'ACCESSADDPICTUREDIRECTLYPAGE','SELECTPICTUREFROMGALLRERYPAGE', 'ADDEDPICTUREDIRECTLY' 'ADDEDPICTURE', 'UPLOADEDPICTURE', 'LINKPICTURETOACTIVITY', 'DELETEPICTUREFROMACTIVITY', 'UNLINKPICTUREFROMACTIVITY', 'DELETEPICTUREFROMGALLERY', 'LOGOFF'], ['LOGIN', 'ACCESSGOALS','ACCESSGOALADDDAILYPAGE', 'ADDEDGOALDAILY', 'ACCESSGOALADDTOTALPAGE','ADDEDGOALTOTAL', 'DELETEGOAL', 'LOGOFF']]

addedContent = np.zeros([len(participants)])

for participant_index in range(0, len(participants)):
    addedActivities = np.sum(activity_timeline[participant_index,:,3])
    addedMeasurements = np.sum(measurement_timeline[participant_index,:,1]) + np.sum(measurement_timeline[participant_index,:,2])
    addedPictures = np.sum(picture_timeline[participant_index,:,5]) + np.sum(picture_timeline[participant_index,:,6])
    addedGoals = np.sum(goal_timeline[participant_index,:,3]) + np.sum(goal_timeline[participant_index,:,5])
    addedContent[participant_index] = addedActivities + addedMeasurements + addedPictures + addedGoals 
np.save('data/cleaned/timeline_analysis_added_content.npy', addedContent)
  
consistency_timeline = np.zeros([len(participants), len(activity_timeline[0])])
for participant_index in range(0, len(participants)):
    for day in range(0, len(activity_timeline[0])):
        if(np.sum(activity_timeline[participant_index, day, 1:8]) > 0 or
        np.sum(measurement_timeline[participant_index, day, 1:8]) > 0 or
        np.sum(picture_timeline[participant_index, day, 1:10]) > 0 or
        np.sum(goal_timeline[participant_index, day, 1:6]) > 0):
            consistency_timeline[participant_index, day] = 1

consistency_times = []
consistency = np.zeros(len(participants))
for participant_index in range(0, len(participants)):
    consistency_times.append([])
    non_zero_consistency_elements = np.nonzero(consistency_timeline[participant_index])
    if len(non_zero_consistency_elements[0]) > 0:    
        consistency_times[participant_index].append(non_zero_consistency_elements[0][0])    
        for index in range(1, len(non_zero_consistency_elements[0])):
            consistency_times[participant_index].append(non_zero_consistency_elements[0][index]- non_zero_consistency_elements[0][index-1])
        consistency_times[participant_index].append(20 - non_zero_consistency_elements[0][-1])
        consistency[participant_index] = np.average(consistency_times[participant_index])
np.save('data/cleaned/timeline_analysis_consistency.npy', consistency)
  
"""
timeline_npy = 'data/cleaned/timeline.npy'
data = np.load(timeline_npy)

temp_flattened = []
for participant_index in range(0, len(data)):
    temp_flattened.append(data[0,:,:].flatten())
cluster_data = np.array(temp_flattened)

y_pred = SpectralClustering(n_clusters=3).fit_predict(cluster_data)
"""
