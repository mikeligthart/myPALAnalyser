import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv
from datetime import datetime, timedelta


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

# Set features
features = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'LOGOFF'],
            ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'LOGOFF'],
            ['LOGIN', 'ACCESSGALLERY', 'ADDEDPICTURE', 'ADDEDPICTUREDIRECTLY', 'LINKPICTURETOACTIVITY','LOGOFF'],
            ['LOGIN', 'ACCESSGOALS','ADDEDGOALDAILY', 'ADDEDGOALTOTAL', 'LOGOFF']]

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

# Build plots using matplotlib
bar_width = 0.35
font_prop = FontProperties()
font_prop.set_size('small')

numberOfParticipants = len(participants)
if (debug):
    numberOfParticipants = 1

for participant_index in range(0, numberOfParticipants):
    #General plot features
    f, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True)
    x = get_list_of_dates(participants[participant_index]['start_date'])
    temp_x = [i for i in range(0, len(x))]
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=9)
    txt = f.text(-0.01, 0.5, '# behaviors', va='center', rotation='vertical')
    plot_title = 'Interaction timeline participant ' + str(participant_index+1)
    ttl = f.text(0.5, 1.01, plot_title, ha='center', size=16)
    dpifig = 300
    if debug:
        dpifig = 72
    
    #Activity features
    for feature_index in range(0, len(features[0])):
        y = activity_timeline[participant_index, :, feature_index]
        bottom = np.sum(activity_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[0][feature_index]
        ax0.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[0][feature_index])
    ax0.set_title('Activities')
    ax0.axvline(stop_data[participant_index], color='r')
    ax0.axvline(half_way[participant_index], color='b')
    lgd0 = ax0.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.31, 1.1), title='Activities')


    #Measurement features
    for feature_index in range(0, len(features[1])):
        y = measurement_timeline[participant_index, :, feature_index]
        bottom = np.sum(measurement_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[1][feature_index]
        ax1.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[1][feature_index])
    ax1.set_title('Measurements')
    ax1.axvline(stop_data[participant_index], color='r')
    ax1.axvline(half_way[participant_index], color='b')
    lgd1 = ax1.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.65, 2.95), title='Measurements')

    #Picture features
    for feature_index in range(0, len(features[2])):
        y = picture_timeline[participant_index, :, feature_index]
        bottom = np.sum(picture_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[2][feature_index]
        ax2.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[2][feature_index])
    ax2.set_title('Pictures')
    ax2.axvline(stop_data[participant_index], color='r')
    ax2.axvline(half_way[participant_index], color='b')
    lgd2 = ax2.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.385, 1.2), title='Pictures')

    #Goal features
    for feature_index in range(0, len(features[3])):
        y = goal_timeline[participant_index, :, feature_index]
        bottom = np.sum(goal_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[3][feature_index]
        ax3.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[3][feature_index])
    ax3.set_title('Goals')
    ax3.set_xlabel("Date")
    ax3.axvline(stop_data[participant_index], color='r')
    ax3.axvline(half_way[participant_index], color='b')
    lgd3 = ax3.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.7, 3.05), title='Goals')

    f.tight_layout()
    
    if save_as == "png" or save_as == "both":

        plt.savefig('data/cleaned/timelines/interaction/interaction_timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(lgd0, lgd1, lgd2, lgd3, txt, ttl, ), bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/interaction/interaction_timeline_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=(lgd0, lgd1, lgd2, lgd3, txt, ttl, ), bbox_inches='tight', format='svg')
    plt.close(f)
