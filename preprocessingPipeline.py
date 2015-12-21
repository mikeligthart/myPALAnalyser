from myPALDataLoader import MyPALDataLoader

userDataLoc = "data/myPAL_userData.json"
measurementDataLoc = "data/myPAL_measurementData.json"

loader = MyPALDataLoader(userDataLoc, measurementDataLoc)
loader.removeUser('hunter')
loader.removeUser('mike.ligthart')
loader.removeUser('elvira')
loader.removeUser('viewer')
loader.buildBaseSets()
