import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv
from datetime import datetime, timedelta
import math

# Settings
debug = False # in debug mode only the plot of only the first participants is created
save_as = "both" #can be saved as png, svg or both

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

# Load metrics
nr_of_logins = np.load('data/cleaned/interaction_logins.npy')
median = np.load('data/cleaned/interaction_median.npy')
iqr = np.load('data/cleaned/interaction_iqr.npy')
total_added = np.load('data/cleaned/interaction_total.npy')

# Set features
features_in_arrays = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'UPDATEACTIVITY', 'DELETEACTIVITY', 'ADDEDACTIVITYTYPE', 'DELETEACTIVITYTYPE', 'LOGOFF'],
            ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'REMOVEDMEASUREMENT', 'UPDATEGLUCOSE', 'UPDATEINSULIN', 'DELETEGLUCOSE', 'DELETEINSULIN', 'LOGOFF'],
            ['LOGIN', 'ACCESSGALLERY', 'ACCESSADDPICTUREPAGE', 'ACCESSADDPICTUREDIRECTLYPAGE','SELECTPICTUREFROMGALLRERYPAGE', 'ADDEDPICTUREDIRECTLY', 'ADDEDPICTURE', 'UPLOADEDPICTURE', 'LINKPICTURETOACTIVITY', 'DELETEPICTUREFROMACTIVITY', 'UNLINKPICTUREFROMACTIVITY', 'DELETEPICTUREFROMGALLERY', 'LOGOFF'],
            ['LOGIN', 'ACCESSGOALS','ACCESSGOALADDDAILYPAGE', 'ADDEDGOALDAILY', 'ACCESSGOALADDTOTALPAGE','ADDEDGOALTOTAL', 'DELETEGOAL', 'LOGOFF']]

features_in_plots = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'LOGOFF'],
            ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'LOGOFF'],
            ['LOGIN', 'ACCESSGALLERY', 'ADDEDPICTUREDIRECTLY', 'ADDEDPICTURE', 'LINKPICTURETOACTIVITY','LOGOFF'],
            ['LOGIN', 'ACCESSGOALS','ADDEDGOALDAILY', 'ADDEDGOALTOTAL', 'LOGOFF']]

feature_indices = []
for plot_nr in range(0, len(features_in_plots)):
    feature_indices.append([])
    for feature in features_in_plots[plot_nr]:
        feature_indices[-1].append(features_in_arrays[plot_nr].index(feature))
               
colors = [["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#7A4900"],
          ["#000000", "#0000A6", "#63FFAC", "#B79762", "#7A4900"],
          ["#000000", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#7A4900"],
          ["#000000","#BA0900", "#6B7900", "#00C2A0", "#7A4900"]]

#Red and blue line to indicate the evaluation session and the half way point    
stop_data=[21, 20, 14, 19, 20, 19, 24, 19, 20, 14, 20, 16, 21, 20]
half_way=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9]

#Helper functions
def get_list_of_dates(start_date_string):
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S').date()
    return [start_date + timedelta(days=x) for x in range(0, 23)]

def get_summary_text(median, iqr, total):
    median = round(median, 1)
    iqr = round(iqr, 1)
    total = round(total, 1)
    if median >= 0:
        return 'median = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
    else:
        return 'No summary\ndetails available'

def get_yticks(y, nr_of_steps):
    max_y = int(math.ceil(np.max(y)))
    y_ticks = range(0, max_y+1)
    y_step_size = int(math.ceil(max_y / nr_of_steps))
    if(y_step_size < 2):
        y_step_size = 1
    else:
        y_step_size = int(math.ceil(y_step_size / 5.0)) * 5
    return y_ticks[0::y_step_size]

# Build plots using matplotlib
bar_width = 0.35
font_prop = FontProperties()
font_prop.set_size('small')

numberOfParticipants = len(participants)
if (debug):
    numberOfParticipants = 1

for participant_index in range(0, numberOfParticipants):
    #Reduce timeline arrays
    activities_for_p = activity_timeline[participant_index, :, feature_indices[0]]
    measurements_for_p = measurement_timeline[participant_index, :, feature_indices[1]]
    pictures_for_p = picture_timeline[participant_index, :, feature_indices[2]]
    goals_for_p = goal_timeline[participant_index, :, feature_indices[3]]
    
    #General plot features
    f, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True)
    x = get_list_of_dates(participants[participant_index]['start_date'])
    temp_x = [i for i in range(0, len(x))]
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=9)
    txt = f.text(-0.01, 0.5, '# behaviors', va='center', rotation='vertical')
    plot_title = 'Interaction timeline participant ' + str(participant_index+1) + ' (#logins = ' + str(int(nr_of_logins[participant_index])) + ')' 
    ttl = f.text(0.5, 1.01, plot_title, ha='center', size=16)
    dpifig = 300
    
    #Activity features
    for feature_index in range(0, len(features_in_plots[0])):
        y = activities_for_p[feature_index, :]
        bottom = np.sum(activities_for_p[0:feature_index, :], axis=0)
        label = features_in_plots[0][feature_index]
        ax0.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[0][feature_index])
    ax0.set_title('Activities')
    ax0.axvline(stop_data[participant_index], color='r')
    ax0.axvline(half_way[participant_index], color='b')
    y_ticks = get_yticks(np.sum(activities_for_p, axis=0), 5)
    ax0.set_yticks(y_ticks)
    ax0.set_yticklabels(y_ticks, size=7)
    lgd0 = ax0.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.51, 1.1), title='Activities')
    metrics0 = f.text(0.98, 0.83, get_summary_text(median[participant_index, 0], iqr[participant_index, 0], total_added[participant_index, 0]), size=7)

    #Measurement features
    for feature_index in range(0, len(features_in_plots[1])):
        y = measurements_for_p[feature_index, :]
        bottom = np.sum(measurements_for_p[0:feature_index, :], axis=0)
        label = features_in_plots[1][feature_index]
        ax1.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[1][feature_index])
    ax1.set_title('Measurements')
    ax1.axvline(stop_data[participant_index], color='r')
    ax1.axvline(half_way[participant_index], color='b')
    y_ticks = get_yticks(np.sum(measurements_for_p, axis=0), 5)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_ticks, size=7)
    lgd1 = ax1.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.85, 2.95), title='Measurements')
    metrics1 = f.text(0.98, 0.605, get_summary_text(median[participant_index, 1], iqr[participant_index, 1], total_added[participant_index, 1]), size=7)
     
    #Picture features
    for feature_index in range(0, len(features_in_plots[2])):
        y = pictures_for_p[feature_index, :]
        bottom = np.sum(pictures_for_p[0:feature_index, :], axis=0)
        label = features_in_plots[2][feature_index]
        ax2.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[2][feature_index])
    ax2.set_title('Pictures')
    ax2.axvline(stop_data[participant_index], color='r')
    ax2.axvline(half_way[participant_index], color='b')
    y_ticks = get_yticks(np.sum(pictures_for_p, axis=0), 5)
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels(y_ticks, size=7)
    lgd2 = ax2.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.585, 1.2), title='Pictures')
    metrics2 = f.text(0.98, 0.38, get_summary_text(median[participant_index, 2], iqr[participant_index, 2], total_added[participant_index, 2]), size=7)

    #Goal features
    for feature_index in range(0, len(features_in_plots[3])):
        y = goals_for_p[feature_index, :]
        bottom = np.sum(goals_for_p[0:feature_index, :], axis=0)
        label = features_in_plots[3][feature_index]
        ax3.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[3][feature_index])
    ax3.set_title('Goals')
    ax3.set_xlabel("Date")
    ax3.axvline(stop_data[participant_index], color='r')
    ax3.axvline(half_way[participant_index], color='b')
    y_ticks = get_yticks(np.sum(goals_for_p, axis=0), 5)
    ax3.set_yticks(y_ticks)
    ax3.set_yticklabels(y_ticks, size=7)
    lgd3 = ax3.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.9, 3.05), title='Goals')
    metrics2 = f.text(0.98, 0.155, get_summary_text(median[participant_index, 3], iqr[participant_index, 3], total_added[participant_index, 3]), size=7)

    f.tight_layout()
    
    if save_as == "png" or save_as == "both":

        plt.savefig('data/cleaned/timelines/interaction/interaction_timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(lgd0, lgd1, lgd2, lgd3, txt, ttl, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/interaction/interaction_timeline_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=(lgd0, lgd1, lgd2, lgd3, txt, ttl, ), bbox_inches='tight', format='svg')
    plt.close(f)
