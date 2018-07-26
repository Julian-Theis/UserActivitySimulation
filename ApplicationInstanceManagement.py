import numpy as np
from collections import deque
from difflib import SequenceMatcher
import random

class ApplicationInstanceManagement():
    """ Managing the opened Applications as well as AppHierarchy """

    """ STATES:
        0 = Closed
        1 = Foreground
        2 = Background
        3 = Minimized
                        """


    def __init__(self, ARRAY_SIZE, maxInstanceExplorer, maxInstanceCalculator, maxInstanceNotepad, timing, logmanager, case):
        self.appHierarchy = []
        self.maxInstanceExplorer = maxInstanceExplorer
        self.maxInstanceCalculator = maxInstanceCalculator
        self.maxInstanceNotepad = maxInstanceNotepad

        self.explorerStates = np.zeros(ARRAY_SIZE, dtype=int)
        self.explorerPaths = ["" for x in range(ARRAY_SIZE)]
        self.notepadStates = np.zeros(ARRAY_SIZE, dtype=int)
        self.notepadFiles = ["" for x in range(ARRAY_SIZE)]
        self.calculatorStates = np.zeros(ARRAY_SIZE, dtype=int)

        self.timing = timing
        self.logmanager = logmanager

        self.case = case


    def isAnyExplorerRunning(self):
        running = False
        if self.explorerStates.sum() > 0:
            running = True
        return running

    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def possibleToOpenNewExplorer(self):
        possible = True
        cnt = 0
        for i in self.explorerStates:
            if i > 0:
                cnt += 1
        if cnt >= self.maxInstanceExplorer:
            possible = False
        return possible

    def getInstance(self, application, purpose, param=[]):
        index = 0
        if(application == "explorer" and purpose == "open"):
            for i in range(len(self.explorerStates)):
                if self.explorerStates[i] == 0:
                    index = i
                    break

        if(application == "explorer" and purpose == "reopen"):
            targetpath = str(param)
            possible_explorer = []
            for i in range(len(self.explorerStates)):
                if self.explorerStates[i] != 0:
                    possible_explorer.append(i)

            if len(possible_explorer) == 1:
                index = possible_explorer[0]
            else:
                metric = -1
                for poss in possible_explorer:
                    met = self.similar(self.explorerPaths[poss], targetpath)
                    if(met > metric):
                        metric = met
                        index = poss

        if (application == "notepad" and purpose == "open"):
            for i in range(len(self.explorerStates)):
                if self.notepadStates[i] == 0:
                    index = i
                    break

        if(application == "calculator" and purpose == "open"):
            for i in range(len(self.calculatorStates)):
                if self.calculatorStates[i] == 0:
                    index = i
                    break

        if(application == "calculator" and purpose == "reopen"):
            possible_calc = []
            for i in range(len(self.calculatorStates)):
                if self.calculatorStates[i] != 0:
                    possible_calc.append(i)

            if len(possible_calc) == 1:
                index = possible_calc[0]
            else:
                selector = random.randint(0, len(possible_calc))
                index = possible_calc[selector]

        return index

    def hierarchyChangeStatusFirstElement(self):
        if len(self.appHierarchy) > 0:
            first = self.appHierarchy[0]
            instance = int(first.split("#")[0][2:])
            application = first.split("#")[1].split(".")[0]

            if application == "notepad" and self.notepadStates[instance]==1:
                self.notepadStates[instance] = 2

            if application == "explorer" and self.explorerStates[instance]==1:
                self.explorerStates[instance] = 2

            if application == "calculator" and self.calculatorStates[instance]==1:
                self.calculatorStates[instance] = 2


    def updateHierarchyOpen(self, pid, process):
        # https://stackoverflow.com/questions/2150108/efficient-way-to-shift-a-list-in-python
        item = str(pid) + "#" + str(process)

        self.hierarchyChangeStatusFirstElement()

        items = deque(self.appHierarchy)
        items.append(item)
        items.rotate(1)
        self.appHierarchy = list(items)

    def updateHierarchyToFG(self, pid, process):
        # https://stackoverflow.com/questions/2150108/efficient-way-to-shift-a-list-in-python
        item = str(pid) + "#" + str(process)
        self.appHierarchy.remove(item)
        self.hierarchyChangeStatusFirstElement()
        items = deque(self.appHierarchy)
        items.append(item)
        items.rotate(1)
        self.appHierarchy = list(items)

    def updateHierarchyClose(self, pid, process):
        # https://stackoverflow.com/questions/2150108/efficient-way-to-shift-a-list-in-python
        item = str(pid) + "#" + str(process)
        self.appHierarchy.remove(item)
        self.hierarchyChangeStatusFirstElement()

    def updateHierarchyMinimize(self, pid, process):
        # https://stackoverflow.com/questions/2150108/efficient-way-to-shift-a-list-in-python
        item = str(pid) + "#" + str(process)
        self.appHierarchy.remove(item)
        self.appHierarchy.append(item)
        self.hierarchyChangeStatusFirstElement()

    def getHierarchyString(self):
        string = "["
        for i in self.appHierarchy:
            if len(string) < 2:
                string = string + i
            else:
                string = string + "," + i
        string = string + "]"
        return string

    def updatePath(self, instance, path):
        self.logmanager.addEvent(str(self.timing.getTime()), "A8",
                                 str("[10" + str(instance) + "," + str(self.explorerPaths[instance]) + "," + str(path) + "]"), self.case)
        self.explorerPaths[instance] = path

    def control(self, application, instance, control, param=[]):
        ## Control Parameter:
        # 0 = closed
        # 1 = open
        # 2 = minimize
        # 4 = maximize / BGtoFG

        self.machineDelay()

        if application == "explorer":
            if control == 0:
                self.explorerStates[instance] = 0
                self.updateHierarchyClose((str(10) + str(instance)), "explorer.exe")
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A2",
                                         str("[10" + str(instance) + ",explorer.exe," + self.explorerPaths[instance] + "]"), self.case)

            elif control == 1:
                self.explorerStates[instance] = 1
                self.updateHierarchyOpen((str(10) + str(instance)), "explorer.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A1",
                                         str("[10" + str(instance) + ",explorer.exe,MAIN,4,4,1,4]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A5",
                                         str("[10" + str(instance) + ",explorer.exe,MAIN]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                       self.getHierarchyString(), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A8",
                                         str("[10" + str(instance) + "," + str(self.explorerPaths[instance]) + ",MAIN]"), self.case)

                self.explorerPaths[instance] = "MAIN"

            elif control == 2:
                self.explorerStates[instance] = 3
                self.updateHierarchyMinimize((str(10) + str(instance)), "explorer.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A4",
                                         str("[10" + str(instance) + ",explorer.exe]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A6",
                                         str("[10" + str(instance) + ",explorer.exe,4,4,-1,-1]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)

            elif control == 3:
                print()


            ######## RECHECK THIS PART, ESPECIALLY THE PREV_STATE PART
            elif control == 4:
                prev_state = self.explorerStates[instance]
                self.explorerStates[instance] = 1
                self.updateHierarchyToFG((str(10) + str(instance)), "explorer.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)

                if prev_state == 3:
                    self.logmanager.addEvent(str(self.timing.getTime()), "A6",
                                             str("[10" + str(instance) + ",explorer.exe,4,4,1,4]"), self.case)
                    self.logmanager.addEvent(str(self.timing.getTime()), "A3",
                                             str("[10" + str(instance) + ",explorer.exe]"), self.case)


        elif application == "notepad":
            if control == 0:
                self.notepadStates[instance] = 0
                self.updateHierarchyClose((str(20) + str(instance)), "notepad.exe")
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A2",
                                         str("[20" + str(instance) + ",notepad.exe," + param + "]"), self.case)

            elif control == 1:
                self.notepadStates[instance] = 1
                self.notepadFiles[instance] = param
                self.updateHierarchyOpen((str(20) + str(instance)), "notepad.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A1",
                                         str("[20" + str(instance) + ",notepad.exe," + param + ",4,4,1,4]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A5",
                                         str("[20" + str(instance) + ",notepad.exe," + param + "]"), self.case)

                self.logmanager.addEvent(str(self.timing.getTime()), "A7", self.getHierarchyString(), self.case)

            elif control == 2:
                self.calculatorStates[instance] = 3
                self.updateHierarchyMinimize((str(20) + str(instance)), "notepad.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A4",
                                         str("[20" + str(instance) + ",notepad.exe]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A6",
                                         str("[20" + str(instance) + ",notepad.exe,4,4,-1,-1]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)

            elif control == 3:
                print()

            elif control == 4:
                prev_state = self.notepadStates[instance]
                self.notepadStates[instance] = 1
                self.updateHierarchyToFG((str(20) + str(instance)), "notepad.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)

                if prev_state == 3:
                    self.logmanager.addEvent(str(self.timing.getTime()), "A6",
                                             str("[20" + str(instance) + ",notepad.exe,4,4,4,4]"), self.case)
                    self.logmanager.addEvent(str(self.timing.getTime()), "A3",
                                             str("[20" + str(instance) + ",notepad.exe]"), self.case)




        elif application == "calculator":
            if control == 0:
                self.calculatorStates[instance] = 0
                self.updateHierarchyClose((str(30) + str(instance)), "calc.exe")
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A2",
                                         str("[30" + str(instance) + ",calc.exe,Calculator]"), self.case)

            elif control == 1:
                self.calculatorStates[instance] = 1
                self.updateHierarchyOpen((str(30) + str(instance)), "calc.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A1",
                                         str("[30" + str(instance) + ",calc.exe,Calculator,4,4,1,4]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A5",
                                         str("[30" + str(instance) + ",calc.exe,Calculator]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A7", self.getHierarchyString(), self.case)

            elif control == 2:
                self.calculatorStates[instance] = 3
                self.updateHierarchyMinimize((str(30) + str(instance)), "calc.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A4",
                                         str("[30" + str(instance) + ",calc.exe]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A6",
                                         str("[30" + str(instance) + ",calc.exe,4,4,-1,-1]"), self.case)
                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)
            elif control == 3:
                print()

            elif control == 4:
                prev_state = self.calculatorStates[instance]
                self.calculatorStates[instance] = 1
                self.updateHierarchyToFG((str(30) + str(instance)), "calc.exe")

                self.logmanager.addEvent(str(self.timing.getTime()), "A7",
                                         self.getHierarchyString(), self.case)

                if prev_state == 3:
                    self.logmanager.addEvent(str(self.timing.getTime()), "A6",
                                             str("[30" + str(instance) + ",calc.exe,4,4,1,4]"), self.case)
                    self.logmanager.addEvent(str(self.timing.getTime()), "A3",
                                             str("[30" + str(instance) + ",calc.exe]"), self.case)

    def isFileOpen(self, filename):
        isOpen = False
        for file in self.notepadFiles:
            if file == filename:
                isOpen = True
                break
        return isOpen

    def getInstanceByFile(self, filename):
        index = -1
        for i in range(len(self.notepadFiles)):
            if self.notepadFiles[i] == filename:
                index = i
                break
        return index


    def machineDelay(self):
        delay = np.random.normal(0.4, 0.1)
        self.timing.delay(delay)




