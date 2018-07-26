import random
import numpy as np

class TaskCompletionManager():
    """ Managing that all tasks get completed """

    def __init__(self, chance_repetition=0.0, max_repetition = 1, beta=0.5):
        self.endSimulation = False
        self.chance_repetition = chance_repetition
        self.max_repetition = max_repetition
        self.current_task = -1
        self.beta = beta
        # https://homepage.divms.uiowa.edu/~mbognar/applets/exp-like.html


        # 0 = Create Summary File
        # 1 = Edit Summary (only possible if task 0 is done)
        # 2 = Read First File
        # 3 = Read Second File
        # 4 = Use Calculator
        self.tasks = [0, 0, 0, 0, 0]

        self.assignTask()


    def taskSequence(self):
        # 0 = Create Summary File
        # 1 = Open Summary
        # 2 = Open File 1
        # 3 = Open File 2
        # 4 = Open Calc
        # 5 = Do math in Calc
        # 6 = Edit and Save Summary

        seq = []
        selectable = [0, 2, 3, 4]
        all = [0,1,2,3,4,5,6]
        rep_limits = [1, self.max_repetition+1, self.max_repetition+1, self.max_repetition+1 ,self.max_repetition+1, 1, 1]

        while(len(selectable) > 0):
            draw = int(np.rint(np.random.exponential(scale=0.6)))

            if draw < len(selectable):
                selected = selectable[draw]

                # Check for the rules
                if (selected == 0) and (selected not in seq):
                    selectable.append(1)


                ## Add selected to sequence
                seq.append(selected)

                ## Complex rules
                if (2 in seq) and (3 in seq) and (4 in seq) and (5 not in seq) and (5 not in selectable):
                    selectable.append(5)

                if (1 in seq) and (5 in seq) and (6 not in selectable):
                    selectable.append(6)


                # if selected can be repeated and given it fulfills repeatability check, keep it in selectable
                for a in all:
                    if a in selectable:
                        counted = seq.count(a)
                        if counted >= rep_limits[a]:
                            #print("remove limit reached", a)
                            selectable.remove(a)
                        elif (counted > 0):
                            if random.random() < (1-self.chance_repetition):
                                #print("remove", a)
                                selectable.remove(a)

                selectable.sort()

            #print("Sequence:", seq)
            #print("Selectable:" ,selectable)
            #print("")

            self.sequence = seq





    def allTasksDone(self):
        done = True
        for i in self.tasks:
            if i < 1:
                done = False
        return done

    def sumTasks(self):
        summed = 0
        for i in self.tasks:
            summed += i
        return summed

    def addTask(self, task):
        self.tasks[task] += 1


    def assignTask(self):
        if self.sumTasks() == 0:
            #possibleTasks = [0,2,3,4]
            possibleTasks = [0]
            self.current_task = random.choice(possibleTasks)

    def taskDone(self, task):
        self.tasks[task] += 1



