import plotly.plotly as py
import plotly.graph_objs as go
import csv
from datetime import datetime, timedelta

activities = []
with open('data/cleaned/activities.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    activities = list(reader)

#x
start_date = datetime(year=2015, month=11, day=26)
date_list = [start_date + timedelta(days=x) for x in range(0, 20)]

#y
data = []
for number in range(1, 14):
    number_of_added_activities = []
    selected_participant = [activity for activity in activities if activity['participant'] == str(number)]
    for date in date_list:
        number_of_added_activities.append(len([activity for activity in selected_participant if datetime.strptime(activity['added'].split('.')[0], '%Y-%m-%d %H:%M:%S').date() == date.date()]))
    data.append(go.Scatter(x=date_list, y=number_of_added_activities))

plot_url = py.plot(data, filename='activities_combined')
