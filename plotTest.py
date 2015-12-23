import plotly.plotly as py
import plotly.graph_objs as go
import csv
from datetime import datetime, timedelta

activities = []
with open('data/cleaned/activities.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    activities = list(reader)

### TIME PLOTS ####
#x
start_date = datetime(year=2015, month=11, day=26)
date_list = [start_date + timedelta(days=x) for x in range(0, 20)]

## Activities ##
#y
addedActivities = []
charactersActivities = []
for number in range(1, 14):
    number_of_added_activities = []
    avarage_character_count = []
    selected_participant = [activity for activity in activities if activity['participant'] == str(number)]
    for date in date_list:
        activities_on_date = [activity for activity in selected_participant if datetime.strptime(activity['added'].split('.')[0], '%Y-%m-%d %H:%M:%S').date() == date.date()]
        number_of_added_activities.append(len(activities_on_date))
        character_count = [len(activity['description']) - activity['description'].count(' ') for activity in activities_on_date]
        if len(character_count):
            avarage_character_count.append(sum(character_count)/float(len(character_count)))
        else:
            avarage_character_count.append(0.0)        
          
    addedActivities.append(go.Scatter(x=date_list, y=number_of_added_activities))
    charactersActivities.append(go.Scatter(x=date_list, y=avarage_character_count))

#plot_url = py.plot(addedActivities, filename='activities_combined')
plot_url2 = py.plot(charactersActivities, filename='activities_characters_combined')    


