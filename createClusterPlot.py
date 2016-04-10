import numpy as np
import csv
import matplotlib.pyplot as plt

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
    

colors = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
"#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
"#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
"#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
"#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
"#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
"#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
"#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
"#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
"#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
"#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
"#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
"#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C"]
area=np.ones([1, 14])*150
area[0,6]=5

added_content_norm = np.linalg.norm(addedContent)
consistency_norm = np.linalg.norm(consistency)

for index in range(0,len(participants)):
    label = 'p' + str(index+1)
    plt.scatter((np.max(consistency) - consistency[index])/consistency_norm, addedContent[index]/added_content_norm, s=area[0,index], c=colors[index], alpha=0.5, label=label)
    
plt.legend(loc=0, scatterpoints = 1, bbox_to_anchor=(1.3, 1.0))
plt.grid()
plt.show()

