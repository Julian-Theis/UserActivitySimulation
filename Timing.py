import math

class Timing():
    """ Class measuring the timing information

    Base units are by default seconds
    """

    current_time = 0

    base_unit = 1000 # representing seconds

    def getTime(self):
        return self.current_time

    def delay(self, delay):
        self.current_time = self.current_time + int(math.floor(delay * self.base_unit))

