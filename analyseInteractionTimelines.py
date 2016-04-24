import numpy as np

# Load timelines numpy
activity_timeline = np.load('data/cleaned/activity_timeline.npy')
measurement_timeline = np.load('data/cleaned/measurement_timeline.npy')
picture_timeline = np.load('data/cleaned/picture_timeline.npy')
goal_timeline = np.load('data/cleaned/goal_timeline.npy')

# General info
feature_names = ['activity_timeline', 'measurement_timeline', 'picture_timeline', 'goal_timeline']
features = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'UPDATEACTIVITY', 'DELETEACTIVITY', 'ADDEDACTIVITYTYPE', 'DELETEACTIVITYTYPE', 'LOGOFF'], ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'REMOVEDMEASUREMENT', 'UPDATEGLUCOSE', 'UPDATEINSULIN', 'DELETEGLUCOSE', 'DELETEINSULIN', 'LOGOFF'], ['LOGIN', 'ACCESSGALLERY', 'ACCESSADDPICTUREPAGE', 'ACCESSADDPICTUREDIRECTLYPAGE','SELECTPICTUREFROMGALLRERYPAGE', 'ADDEDPICTUREDIRECTLY' 'ADDEDPICTURE', 'UPLOADEDPICTURE', 'LINKPICTURETOACTIVITY', 'DELETEPICTUREFROMACTIVITY', 'UNLINKPICTUREFROMACTIVITY', 'DELETEPICTUREFROMGALLERY', 'LOGOFF'], ['LOGIN', 'ACCESSGOALS','ACCESSGOALADDDAILYPAGE', 'ADDEDGOALDAILY', 'ACCESSGOALADDTOTALPAGE','ADDEDGOALTOTAL', 'DELETEGOAL', 'LOGOFF']]
nr_of_participants = int(activity_timeline.shape[0])

def calc_median(y):
    nonzero_y = y[y.nonzero()]
    if nonzero_y.size > 0:
        return np.median(nonzero_y)
    else:
        return -1

def calc_iqr(y):
    nonzero_y = y[y.nonzero()]
    if nonzero_y.size > 0:
        return np.subtract(*np.percentile(nonzero_y, [75, 25]))
    else:
        return -1


#Added content
addedContent = np.zeros([nr_of_participants])
median = np.ones([nr_of_participants, 4]) * -1
iqr = np.ones([nr_of_participants, 4]) * -1
total = np.zeros([nr_of_participants, 4])
logins = np.zeros([nr_of_participants])
for participant_index in range(0, nr_of_participants):
    
    addedActivities = activity_timeline[participant_index,:,3]
    addedMeasurements = measurement_timeline[participant_index,:,1] + measurement_timeline[participant_index,:,2]
    addedPictures = picture_timeline[participant_index,:,5] + picture_timeline[participant_index,:,6]
    addedGoals = goal_timeline[participant_index,:,3] + goal_timeline[participant_index,:,5]
      
    median[participant_index, 0] = calc_median(addedActivities)
    median[participant_index, 1] = calc_median(addedMeasurements)
    median[participant_index, 2] = calc_median(addedPictures)
    median[participant_index, 3] = calc_median(addedGoals)
    
    iqr[participant_index, 0] = calc_iqr(addedActivities)
    iqr[participant_index, 1] = calc_iqr(addedMeasurements)
    iqr[participant_index, 2] = calc_iqr(addedPictures)
    iqr[participant_index, 3] = calc_iqr(addedGoals)
    
    total[participant_index, 0] = np.sum(addedActivities)
    total[participant_index, 1] = np.sum(addedMeasurements)
    total[participant_index, 2] = np.sum(addedPictures)
    total[participant_index, 3] = np.sum(addedGoals)
    
    addedContent[participant_index] = np.sum(total[participant_index, :])
    logins[participant_index] = np.sum(activity_timeline[participant_index,:,0])

np.save('data/cleaned/interaction_median.npy', median)
np.save('data/cleaned/interaction_iqr.npy', iqr)
np.save('data/cleaned/interaction_total.npy', total)
np.save('data/cleaned/interaction_logins.npy', logins)
np.save('data/cleaned/timeline_analysis_added_content.npy', addedContent)

#Consistency
consistency_timeline = np.zeros([nr_of_participants, len(activity_timeline[0])])
for participant_index in range(0, nr_of_participants):
    for day in range(0, len(activity_timeline[0])):
        if(np.sum(activity_timeline[participant_index, day, 1:8]) > 0 or
        np.sum(measurement_timeline[participant_index, day, 1:8]) > 0 or
        np.sum(picture_timeline[participant_index, day, 1:10]) > 0 or
        np.sum(goal_timeline[participant_index, day, 1:6]) > 0):
            consistency_timeline[participant_index, day] = 1

consistency_times = []
consistency = np.zeros([nr_of_participants])
for participant_index in range(0, nr_of_participants):
    consistency_times.append([])
    non_zero_consistency_elements = np.nonzero(consistency_timeline[participant_index])
    if len(non_zero_consistency_elements[0]) > 0:    
        consistency_times[participant_index].append(non_zero_consistency_elements[0][0])    
        for index in range(1, len(non_zero_consistency_elements[0])):
            consistency_times[participant_index].append(non_zero_consistency_elements[0][index]- non_zero_consistency_elements[0][index-1])
        consistency_times[participant_index].append(20 - non_zero_consistency_elements[0][-1])
        consistency[participant_index] = np.average(consistency_times[participant_index])
np.save('data/cleaned/timeline_analysis_consistency.npy', consistency)
