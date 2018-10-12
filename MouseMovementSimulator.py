import numpy as np
import random

class MouseMovementManager():
    """ Simulates the movement of the mouse """

    def __init__(self, timing, logmanager, mouse_precision, reactivity, case, hllog):
        self.timing = timing
        self.logmanager = logmanager
        self.mouse_X = 4
        self.mouse_Y = 1
        self.precision = mouse_precision
        self.reactivity = reactivity
        self.case = case

        self.hllog = hllog

    def move(self, target_x, target_y):

        while ((self.mouse_X != target_x) or (self.mouse_Y != target_y)):
             if (random.random() < 0.5):
                 if(self.mouse_X != target_x):
                     leftOright = 0
                     if self.mouse_X > target_x:
                         leftOright = -1
                     else:
                         leftOright = 1

                     ## Decide based on Precision ##
                     if (leftOright == -1):
                         if random.random() > self.precision:
                             if random.random() < 0.5:
                                 leftOright = 0
                             else:
                                 leftOright = 1
                     elif leftOright == 1:
                         if random.random() > self.precision:
                             if random.random() < 0.5:
                                 leftOright = 0
                             else:
                                 leftOright = -1

                     ## Check Boundaries
                     if(self.mouse_X == 4 and leftOright == 1) or (self.mouse_X == 1 and leftOright == -1):
                         leftOright = 0


                     self.moveDelay()
                     self.mouse_X += leftOright
                     self.logmanager.addEvent(str(self.timing.getTime()), "M",
                                              str("[" + str(self.mouse_X) + "," + str(self.mouse_Y) + "]"), self.case)
                     self.hllog.addEvent(str(self.timing.getTime()), "mouse to " + str(self.mouse_X) + "," + str(self.mouse_Y) , self.case)


             else:
                 if self.mouse_Y != target_y:
                     downOup = 0
                     if self.mouse_Y > target_y:
                         downOup = -1
                     else:
                         downOup = 1

                     ## Decide based on Precision ##
                     if (downOup == -1):
                         if random.random() > self.precision:
                             if random.random() < 0.5:
                                 downOup = 0
                             else:
                                 downOup = 1
                     elif (downOup == 1):
                         if random.random() > self.precision:
                             if random.random() < 0.5:
                                 downOup = 0
                             else:
                                 downOup = -1

                     ## Check Boundaries
                     if (self.mouse_Y == 4 and downOup == 1) or (self.mouse_Y == 1 and downOup == -1):
                         downOup = 0

                     self.moveDelay()
                     self.mouse_Y += downOup
                     self.logmanager.addEvent(str(self.timing.getTime()), "M", str("[" + str(self.mouse_X) + "," + str(self.mouse_Y) + "]"), self.case)
                     self.hllog.addEvent(str(self.timing.getTime()),
                                     "mouse to " + str(self.mouse_X) + "," + str(self.mouse_Y), self.case)


    def moveDelay(self):
        delay = np.random.normal( (0.3 + self.reactivity), 0.08)
        self.timing.delay(delay)

    def click(self):
        self.clickDelay()
        self.logmanager.addEvent(str(self.timing.getTime()), "K3",
                                 str("[1," + str(self.mouse_X) + "," + str(self.mouse_Y) + "]"), self.case)

        self.hllog.addEvent(str(self.timing.getTime()), "mouse click", self.case)

    def rightclick(self):
        self.clickDelay()
        self.logmanager.addEvent(str(self.timing.getTime()), "K3",
                                 str("[2," + str(self.mouse_X) + "," + str(self.mouse_Y) + "]"), self.case)

        self.hllog.addEvent(str(self.timing.getTime()), "mouse rightclick", self.case)

    def doubleclick(self):
        self.clickDelay()
        self.logmanager.addEvent(str(self.timing.getTime()), "K3",
                                 str("[1," + str(self.mouse_X) + "," + str(self.mouse_Y) + "]"), self.case)
        self.doubleclickDelay()
        self.logmanager.addEvent(str(self.timing.getTime()), "K3",
                                 str("[1," + str(self.mouse_X) + "," + str(self.mouse_Y) + "]"), self.case)

        self.hllog.addEvent(str(self.timing.getTime()), "mouse doubleclick", self.case)

    def clickDelay(self):
        delay = np.random.normal((0.15 + (self.reactivity * 0.2)), 0.03)
        self.timing.delay(delay)

    def doubleclickDelay(self):
        delay = np.random.normal((0.05 + (self.reactivity * 0.1)), 0.01)
        self.timing.delay(delay)
