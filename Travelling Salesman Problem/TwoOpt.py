import copy

from Constant import Constant


class TwoOpt:

    def __init__(self, graph, nearestSolutionList, savingSolutionList):
        self.graph = graph
        self.vis = [False] * graph.n
        self.nearestSolutionList = nearestSolutionList
        self.savingSolutionList = savingSolutionList

        self.neighborAvgCost = 0
        self.neighborBestCost = Constant.INF
        self.neighborWorstCost = 0

        self.savingAvgCost = 0
        self.savingBestCost = Constant.INF
        self.savingWorstCost = 0

        self.bestInFirstImprove = Constant.INF
        self.bestInBestImprove = Constant.INF

    def firstImprove(self):
        solutionList = self.nearestSolutionList
        for m in range(2):
            totalCost = 0
            if m == 1: solutionList = self.savingSolutionList
            k = 0
            while k < len(solutionList):
                curSolution = solutionList[k]
                curCost = solutionList[k].getCostOfTour()
                chnged = False
                for i in range(0, len(curSolution.solutionPath)):
                    for j in range(i + 2, len(curSolution.solutionPath) - 1):
                        curSolution.solutionPath[i + 1:j + 1] = curSolution.solutionPath[j:i:-1]  # reverse list
                        if curSolution.getCostOfTour() < curCost:  # first Choice Hill Climbing
                            chnged = True
                            break
                        curSolution.solutionPath[i + 1:j + 1] = curSolution.solutionPath[j:i:-1]  # reverse list
                    if chnged: break
                solCost = solutionList[k].getCostOfTour()
                if m == 0:
                    self.neighborBestCost = min(self.neighborBestCost, solCost)
                    self.neighborWorstCost = max(self.neighborWorstCost, solCost)
                else:
                    self.savingBestCost = min(self.savingBestCost, solCost)
                    self.savingWorstCost = max(self.savingWorstCost, solCost)
                if not chnged:
                    totalCost += solCost
                    k += 1
            if m == 0:
                self.neighborAvgCost = totalCost / len(self.nearestSolutionList)
            else:
                self.savingAvgCost = totalCost / len(self.savingSolutionList)
            self.bestInFirstImprove = min(self.savingBestCost, self.neighborBestCost)

    def bestImprove(self):
        solutionList = self.nearestSolutionList
        for m in range(2):
            totalCost = 0

            if m == 1: solutionList = self.savingSolutionList
            minCost = Constant.INF
            minSolution = copy.deepcopy(solutionList[0])
            k = 0
            while k < len(solutionList):

                curSolution = solutionList[k]
                curCost = solutionList[k].getCostOfTour()
                chngd = False
                for i in range(0, len(curSolution.solutionPath)):
                    for j in range(i + 2, len(curSolution.solutionPath)):
                        curSolution.solutionPath[i + 1:j + 1] = curSolution.solutionPath[j:i:-1]  #
                        tmpCost = curSolution.getCostOfTour()

                        if tmpCost < minCost:
                            minCost = tmpCost
                            minSolution = copy.deepcopy(curSolution)
                        curSolution.solutionPath[i + 1:j + 1] = curSolution.solutionPath[j:i:-1]  #

                if minCost < curCost:  # steepest ascent hill-climbing
                    solutionList[k] = minSolution
                    chngd = True
                solCost = solutionList[k].getCostOfTour()

                if m == 0:
                    self.neighborBestCost = min(self.neighborBestCost, solCost)
                    self.neighborWorstCost = max(self.neighborWorstCost, solCost)
                else:
                    self.savingBestCost = min(self.savingBestCost, solCost)
                    self.savingWorstCost = max(self.savingWorstCost, solCost)
                if not chngd:
                    totalCost += solCost
                    k += 1

            if m == 0:
                self.neighborAvgCost = totalCost / len(self.nearestSolutionList)
            else:
                self.savingAvgCost = totalCost / len(self.savingSolutionList)
            self.bestInBestImprove = min(self.savingBestCost, self.neighborBestCost)
