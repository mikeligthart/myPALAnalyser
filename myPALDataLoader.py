import json
from pprint import pprint
from operator import itemgetter
from datetime import datetime

class MyPALDataLoader:

    def __init__(self, userDataLoc, measurementDataLoc):
        with open(userDataLoc) as userDataFile:
            self.userData = json.load(userDataFile)
        with open(measurementDataLoc) as measurementDataFile:
            self.measurementData = json.load(measurementDataFile)

    def removeUser(self, userName):
        for index in range(0, len(self.userData)):
            if self.userData[index]['userName'] == userName:
                del self.userData[index]
                break

    def buildBaseSets(self):
        self.baseActivities = [self._buildBaseActivities(userdata['diaryActivities']) for userdata in self.userData]

    def _buildBaseActivities(self, rawActivities):
        activities = []
        for index in range(0, len(rawActivities)):
            activities.append({})
            activities[index]['participant'] = self._changeNameForNumber(rawActivities[index]['userName'])
            activities[index]['added'] = datetime.fromtimestamp(rawActivities[index]['added']/1000.0)
            activities[index]['start'] = datetime.strptime(rawActivities[index]['date'] + ' ' + rawActivities[index]['starttime'], '%Y-%m-%d %H:%M:%S')
            activities[index]['end'] = datetime.strptime(rawActivities[index]['date'] + ' ' + rawActivities[index]['endtime'], '%Y-%m-%d %H:%M:%S')
            activities[index]['name'] = rawActivities[index]['name']
            activities[index]['description'] = rawActivities[index]['description']
            activities[index]['emotion'] = rawActivities[index]['emotion']
            try:
                activities[index]['picture'] = rawActivities[index]['picture']['name']
            except TypeError:
                activities[index]['picture'] = None
                
        return sorted(activities, key=itemgetter('added'))
        
    def _changeNameForNumber(self, name):
        numberForName = ['benja', 'sinne', 'daan', 'tom', 'rick', 'martijn', 'hunter', 'ilse', 'casper', 'safiye', 'yasmin', 'koen', 'maas', 'janwillem']
        return 1 + numberForName.index(name)
