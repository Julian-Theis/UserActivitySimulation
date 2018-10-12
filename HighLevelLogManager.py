import pandas as pd

class HighLevelLogManager():
    """ Log File Buffer """

    def __init__(self, filename):
        self.filename = filename
        self.data = pd.DataFrame(columns=['time', 'event', 'case'])

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def addEvent(self, time, event, case):
        frame = pd.DataFrame([{'time' : str(time), 'event': str(event), 'case': str(case)}])
        self.data = pd.concat([self.data, frame])

    def writeToCsv(self):
        self.data.to_csv(self.filename, sep=",", index=False, header=False, columns=['time', 'event', 'case'])