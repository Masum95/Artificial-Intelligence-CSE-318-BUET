from Graph import *


class Solution:

    def __init__(self, graph):
        self.solutionPath = []
        self.graph = graph
        self.cost = 0

    def getStartingNode(self):
        return self.solutionPath[0]

    def append(self,n):
        self.solutionPath.append(n)

    def getCostOfTour(self):
        cost = 0
        list = self.solutionPath
        lastIndxOfList = len(list)

        for i in range(0, len(list)):
            cost += self.graph.adjMat[list[i]][list[(i + 1) % lastIndxOfList]]
        self.cost = cost
        return cost

    def printPath(self):

        print("Cost of Tour -> ", self.getCostOfTour(), "\n")

        i, j = 0, 0
        while i < len(self.graph.pointList):
            while j < min(i + 4, len(self.graph.pointList)):
                print(self.solutionPath[j], " ->", end=" ")
                j += 1
            i = j
            print("")
        print(self.solutionPath[0])


    @staticmethod
    def insertIntoBest1(list, solutionToAdd):
        if len(list) == 1:
            maxCost, indx = 0, 0
            for i in range(0, len(list)):
                if list[i].cost > maxCost:
                    maxCost, indx = list[i].cost, i

            if maxCost > solutionToAdd.cost:
                del list[indx]
                list.append(solutionToAdd)
        else:
            list.append(solutionToAdd)

    @staticmethod
    def insertIntoBest4(list, solutionToAdd):
        if len(list) == 4:
            maxCost, indx = 0, 0
            for i in range(0, len(list)):
                if list[i].cost > maxCost:
                    maxCost, indx = list[i].cost, i

            if maxCost > solutionToAdd.cost:
                del list[indx]
                list.append(solutionToAdd)
        else:
            list.append(solutionToAdd)

    def __str__(self) :
        return str(self.solutionPath) + "\n" + str(self.cost)

