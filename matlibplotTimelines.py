import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv
from datetime import datetime, timedelta

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
features = [['LOGIN', 'TOGETHERORSELF', 'TOGETHER','ADDEDACTIVITY', 'VIEWACTIVITY', 'UPDATEACTIVITY', 'DELETEACTIVITY', 'ADDEDACTIVITYTYPE', 'DELETEACTIVITYTYPE', 'LOGOFF'],
            ['LOGIN', 'ADDEDGLUCOSE', 'ADDEDINSULIN', 'VIEWMEASUREMENT', 'UPDATEGLUCOSE', 'UPDATEINSULIN', 'DELETEGLUCOSE', 'DELETEINSULIN', 'LOGOFF'],
            ['LOGIN', 'ACCESSGALLERY', 'ADDEDPICTURE', 'SELECTPICTUREFROMGALLRERYPAGE', 'ADDEDPICTUREDIRECTLY', 'LINKPICTURETOACTIVITY', 'DELETEPICTUREFROMACTIVITY', 'UNLINKPICTUREFROMACTIVITY', 'DELETEPICTUREFROMGALLERY', 'LOGOFF'],
            ['LOGIN', 'ACCESSGOALS','ADDEDGOALDAILY', 'ADDEDGOALTOTAL', 'DELETEGOAL', 'LOGOFF']]

colors = [["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059", "#FFDBE5", "#7A4900"],
          ["#000000", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87", "#5A0007", "#7A4900"],
          ["#000000", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80", "#61615A", "#7A4900"],
          ["#000000","#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#7A4900"]]
    
 
"""
["#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
"#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
"#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
"#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
"#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
"#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
"#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
"#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
"#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
"#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C"]
"""
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

for participant_index in range(0, len(participants)):
    f, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True)
    x = get_list_of_dates(participants[participant_index]['start_date'])
    temp_x = [i for i in range(0, len(x))]
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=11)
    txt = f.text(-0.01, 0.5, '# behaviors', va='center', rotation='vertical')
    plot_title = 'Interaction profile participant ' + str(participant_index+1)
    ttl = f.text(0.5, 1.01, plot_title, ha='center', size=16)
    
    #Activity features
    for feature_index in range(0, len(features[0])):
        y = activity_timeline[participant_index, :, feature_index]
        bottom = np.sum(activity_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[0][feature_index]
        ax0.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[0][feature_index])
    ax0.set_title('Activities')
    ax0.axvline(stop_data[participant_index], color='r')
    ax0.axvline(half_way[participant_index], color='b')
    lgd0 = ax0.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.3, 1.1), title='Activities')


    #Measurement features
    for feature_index in range(0, len(features[1])):
        y = measurement_timeline[participant_index, :, feature_index]
        bottom = np.sum(measurement_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[1][feature_index]
        ax1.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[1][feature_index])
    ax1.set_title('Measurements')
    ax1.axvline(stop_data[participant_index], color='r')
    ax1.axvline(half_way[participant_index], color='b')
    lgd1 = ax1.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.6, 2.6), title='Measurements')

    #Picture features
    for feature_index in range(0, len(features[2])):
        y = picture_timeline[participant_index, :, feature_index]
        bottom = np.sum(picture_timeline[participant_index, :, 0:feature_index], axis=1)
        label = features[2][feature_index]
        ax2.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[2][feature_index])
    ax2.set_title('Pictures')
    ax2.axvline(stop_data[participant_index], color='r')
    ax2.axvline(half_way[participant_index], color='b')
    lgd2 = ax2.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.45, 1.2), title='Pictures')

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
    lgd3 = ax3.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.725, 2.5), title='Goals')

    f.tight_layout()
    plt.savefig('data/cleaned/plots/timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=(lgd0, lgd1, lgd2, lgd3, txt, ttl, ), bbox_inches='tight')
    plt.close(f)
