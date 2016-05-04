import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv
from datetime import datetime, timedelta
import math

# Settings
debug = False # in debug mode only the plot of only the first participants is created
save_as = "png" #can be saved as png, svg or both
number_of_days = 23
with_legend = [True, False, False, False, False, False, False, False, False, False, False, False, False, False]

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

avatar_interaction = np.load('data/cleaned/avatar_interaction.npy')

login_time = np.load('data/cleaned/login_time.npy')
average_nr_of_words = np.load('data/cleaned/average_nr_of_words.npy')
personal_score = np.load('data/cleaned/personal_score.npy')
goal_difficulity = np.load('data/cleaned/goal_difficulty.npy')

# Load metrics
nr_of_logins = np.load('data/cleaned/interaction_logins.npy')
added_content = np.load('data/cleaned/timeline_analysis_added_content.npy')
consistency = 1 / np.load('data/cleaned/timeline_analysis_consistency.npy')

median = np.c_[np.load('data/cleaned/interaction_median.npy'), np.load('data/cleaned/avatar_median.npy'), np.load('data/cleaned/content_median.npy')]
iqr =np.c_[np.load('data/cleaned/interaction_iqr.npy'), np.load('data/cleaned/avatar_iqr.npy'), np.load('data/cleaned/content_iqr.npy')]
total = np.c_[np.load('data/cleaned/interaction_total.npy'), np.load('data/cleaned/avatar_total.npy'), np.load('data/cleaned/content_total.npy')]


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

def get_summary_text(median, iqr, total, median2 = None, iqr2 = None, total2 = None):
    median = round(median, 1)
    iqr = round(iqr, 1)
    total = round(total, 1)
    if median2 is None:
        if median >= 0:
            return 'median = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
        else:
            return 'No summary\ndetails available'
    else:
        median2 = round(median2, 1)
        iqr2 = round(iqr2, 1)
        total2 = round(total2, 1)
        if median >= 0 and median2 >= -1:
            return '              D      T \nmedian: ' + str(median) + '    '+ str(median2) +'\nIQR:       '+ str(iqr) +'    ' + str(iqr2) + '\ntotal:     ' + str(total) + '  '+ str(total2)
        elif median >= 0 and median2 == -1:
            return 'Daily:\nmedian = ' + str(median) + '\nIQR = ' + str(iqr) + '\nTotal = ' + str(total)
        elif median == -1 and median2 >= 0:
            return 'Total:\nmedian = ' + str(median2) + '\nIQR = ' + str(iqr2) + '\nTotal = ' + str(total2)
        else:   
            return 'No summary\ndetails available'

def set_y_lim(ax, y, y_lim, y_range, bars, bars2 = None):
    ax.set_yticks(range(y_lim + 1)[0::y_range])
    ax.set_yticklabels(range(y_lim + 1)[0::y_range], size=7)
    ax.set_ylim([0,y_lim])
    if not bars2:
        for index in np.where(y > y_lim)[0]:
            rect = bars[index]
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.8, '%d' % int(height), ha='center', va='bottom', size=5)
    else:
        for index in range(0, len(y)):
            rect1 = bars[index]
            rect2 = bars2[index]
            h1 = rect1.get_height()
            h2 = rect2.get_height()
            if (h1 + h2) > y_lim:
                ax.text(rect1.get_x() + rect1.get_width()/2., 0.5, 'd: %d' % int(h1), ha='center', va='bottom', size=5)
                ax.text(rect2.get_x() + rect2.get_width()/2., 10, 't: %d' % int(h2), ha='center', va='bottom', size=5)
    return ax

def get_y_color(y, y_lim):
    y_color = np.repeat(np.array(['b']), len(y))
    y_color[y > y_lim] = 'r'
    return y_color

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

#In debug mode only 1 timeline will be rendered
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
    f, (ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(9, sharex=True, figsize=(8,9.5))
    x = get_list_of_dates(participants[participant_index]['start_date'])
    temp_x = [i for i in range(0, len(x))]
    tick_pos = [i+(bar_width/2) for i in range(0, len(x))]
    ticks = [datetime.strftime(date, '%d %b') for date in x]
    plt.xticks(tick_pos[0::2], ticks[0::2], size=9)
    txt = f.text(0.01, 0.75, '# behaviors', va='center', rotation='vertical')
    plot_title = 'Interaction timeline participant ' + str(participant_index+1) + '\n#logins = ' + str(int(nr_of_logins[participant_index])) + ', added content = ' + str(added_content[participant_index]) + ', consistency = ' + str(consistency[participant_index])
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
    lgd0 = ax0.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.39, 1.1), title='Activities')
    metrics0 = f.text(0.98, 0.925, get_summary_text(median[participant_index, 0], iqr[participant_index, 0], total[participant_index, 0]), size=7)

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
    lgd1 = ax1.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.63, 2.95), title='Measurements')
    metrics1 = f.text(0.98, 0.82, get_summary_text(median[participant_index, 1], iqr[participant_index, 1], total[participant_index, 1]), size=7)
     
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
    lgd2 = ax2.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.45, 1.2), title='Pictures')
    metrics2 = f.text(0.98, 0.71, get_summary_text(median[participant_index, 2], iqr[participant_index, 2], total[participant_index, 2]), size=7)

    #Goal features
    for feature_index in range(0, len(features_in_plots[3])):
        y = goals_for_p[feature_index, :]
        bottom = np.sum(goals_for_p[0:feature_index, :], axis=0)
        label = features_in_plots[3][feature_index]
        ax3.bar(temp_x, y, width=bar_width, bottom=bottom, label=label, alpha=0.5, color=colors[3][feature_index])
    ax3.set_title('Goals')
    ax3.axvline(stop_data[participant_index], color='r')
    ax3.axvline(half_way[participant_index], color='b')
    y_ticks = get_yticks(np.sum(goals_for_p, axis=0), 5)
    ax3.set_yticks(y_ticks)
    ax3.set_yticklabels(y_ticks, size=7)
    lgd3 = ax3.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.69, 3.05), title='Goals')
    metrics3 = f.text(0.98, 0.6, get_summary_text(median[participant_index, 3], iqr[participant_index, 3], total[participant_index, 3]), size=7)

    ## AVATAR INTERACTION ##
    y = avatar_interaction[participant_index, 0:number_of_days]
    y_lim = 45
    y_range = 5

    #plot
    bars = ax4.bar(temp_x, y, width=bar_width, color=get_y_color(y, y_lim))
    ax4 = set_y_lim(ax4, y, y_lim, y_range, bars)
    
    #labels and lines    
    ax4.set_title('Avatar Interaction')
    y_lbl4 = ax4.set_ylabel("#Interactions")
    ax4.axvline(stop_data[participant_index], color='r')
    ax4.axvline(half_way[participant_index], color='b')
    
    #metrics
    metrics4 = f.text(0.98, 0.49, get_summary_text(median[participant_index, 4], iqr[participant_index, 4], total[participant_index, 4]), size=7)

    ## LOGIN TIME ##
    y = login_time[participant_index, 0:number_of_days]/60
    y_lim = 50    
    y_range = 10
    
    #plot
    bars = ax5.bar(temp_x, y, width=bar_width, color=get_y_color(y, y_lim))
    ax5 = set_y_lim(ax5, y, y_lim, y_range, bars)
    
    #labels and lines    
    ax5.set_title('Login time')
    y_lbl5 = ax5.set_ylabel("Minutes")
    ax5.axvline(stop_data[participant_index], color='r')
    ax5.axvline(half_way[participant_index], color='b')  

    #metrics
    metrics5 = f.text(0.98, 0.39, get_summary_text(median[participant_index, 5], iqr[participant_index, 5], total[participant_index, 5]), size=7)

    ## NUMBER OF WORDS ##
    y = average_nr_of_words[participant_index, 0:number_of_days] 
    y_lim = 25
    y_range = 5    
    
    #plot
    bars = ax6.bar(temp_x, y, width=bar_width, color=get_y_color(y, y_lim))
    ax6 = set_y_lim(ax6, y, y_lim, y_range, bars)

    #labels and lines     
    ax6.set_title('Average number of words')    
    y_lbl6 = ax6.set_ylabel("# words")
    ax6.axvline(stop_data[participant_index], color='r')
    ax6.axvline(half_way[participant_index], color='b')
    
    #Metrics
    metrics6 = f.text(0.98, 0.28, get_summary_text(median[participant_index, 6], iqr[participant_index, 6], total[participant_index, 6]), size=7)
    
    ## PERSONAL LEVEL ##
    y = personal_score[participant_index, 0:number_of_days]
    ax7.bar(temp_x, y, width=bar_width)
    ax7.set_title('Personal level of added content')
    y_lbl7 = ax7.set_ylabel("Personal level")
    y_ticks = [0, 1, 2, 3, 4]
    ax7.set_yticks(y_ticks)
    ax7.set_yticklabels(y_ticks, size=7)
    ax7.axvline(stop_data[participant_index], color='r')
    ax7.axvline(half_way[participant_index], color='b')
    metrics7 = f.text(0.98, 0.17, get_summary_text(median[participant_index, 7], iqr[participant_index, 7], total[participant_index, 7]), size=7)

    ## GOAL DIFFICULTY ##
    y_daily = goal_difficulity[participant_index, 0:number_of_days, 0]    
    y_total = goal_difficulity[participant_index, 0:number_of_days, 1]
    y_lim = 10
    y_range = 2
      
    #plot
    bars1 = ax8.bar(temp_x, y_daily, width=bar_width, color='b', label='Daily Goals')
    bars2 = ax8.bar(temp_x, y_total, width=bar_width, bottom=y_daily, color='c', label='Total Goals')
    ax8 = set_y_lim(ax8, y_daily, y_lim, y_range, bars1, bars2)
    
    #labels and lines
    ax8.set_title('Goal difficulty')
    y_lbl8 = ax8.set_ylabel("Difficulty")
    ax8.set_xlabel("Date")
    ax8.axvline(stop_data[participant_index], color='r')
    ax8.axvline(half_way[participant_index], color='b')
    
    #metrics and legend
    lgd8 = ax8.legend(prop = font_prop, loc='upper right', bbox_to_anchor=(1.35, 1.23), title='Goals')
    metrics8 = f.text(0.98, 0.06, get_summary_text(median[participant_index, 8], iqr[participant_index, 8], total[participant_index, 8], median[participant_index, 9], iqr[participant_index, 9], total[participant_index, 9]), size=7)

    f.tight_layout()

    if with_legend[participant_index]:
        bbox_extra = (lgd0, lgd1, lgd2, lgd3, lgd8, txt, ttl, )
    else:
        bbox_extra = (metrics0, metrics8, txt, ttl, )
    
    if save_as == "png" or save_as == "both":
        plt.savefig('data/cleaned/timelines/interaction/interaction_timeline_p' + str(participant_index + 1) + '.png', bbox_extra_artists=bbox_extra, bbox_inches='tight', dpi=dpifig)
    if save_as == "svg" or save_as == "both":
        plt.savefig('data/cleaned/timelines/interaction/interaction_timeline_p' + str(participant_index + 1) + '.svg', bbox_extra_artists=bbox_extra, bbox_inches='tight', format='svg')
    plt.close(f)
