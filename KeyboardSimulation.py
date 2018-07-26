import numpy as np
import random

class KeyboardManager():
    """ Manages the Keyboard inputs """

    def __init__(self, timing, logmanager, keyprecision, reactivity, case):
        self.timing = timing
        self.logmanager = logmanager
        self.precision = keyprecision
        self.reactivity = reactivity
        self.case = case
        self.numKeys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=']

    def write(self, buffer):
        if (buffer[0] == "#") and (buffer[len(buffer)-1] == "#"):
            key = buffer[1:len(buffer)-1]
            self.delay()
            self.logmanager.addEvent(str(self.timing.getTime()), "K1",
                                     str("[" + str(key) + "]"), self.case)
        else:
            i = 0
            while i < len(buffer):
                self.delay()
                key = buffer[i]
                if key in self.numKeys:
                    out = "NUM"
                else:
                    out = "TEXT"
                self.logmanager.addEvent(str(self.timing.getTime()), "K1",
                                         str("[" + str(out) + "]"), self.case)
                if random.random() < self.precision:
                    i = i + 1

    def delay(self):
        delay = np.absolute(np.random.normal((0.4 + (self.reactivity*0.5)), 0.1))
        self.timing.delay(delay)