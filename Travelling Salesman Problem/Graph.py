
from Node import Node
from Constant import Constant
from random import *
from NearestNeighbor import NearestNeighbor
from SavingHeuristic import SavingHeuristic
from TwoOpt import TwoOpt


class Graph:

    def __init__(self, n, whichInput):
        self.n = n
        self.adjMat = [[0] * n for i in range(n)]  # initializing a 2 d matrix of n*n size
        self.pointList = []                        # Given list of points on cartesian co-ordinate
        self.vis = [False] * n
        self.solutionPath = []
        self.whichInput = whichInput

    def printPerformance(self,whichHeuristic,nearestNeighbor, saving):
        print()
        print("---------", whichHeuristic, "----------")
        firstTab = 8
        print("\t\t\t\tAvg Case %s|   Best Case %s|    Worst Case"%("\t"*firstTab, "\t"*firstTab))
        print("-"*250)
        print("NH ->\t\t\t  ", nearestNeighbor.avgCost," \t\t\t\t\t|",nearestNeighbor.bestCost," \t\t\t\t\t\t|",nearestNeighbor.worstCost)
        print("SH ->\t\t\t  ", saving.avgCost," \t\t\t\t\t|",saving.bestCost," \t\t\t\t\t\t|",saving.worstCost)

    def runHeuristic(self):
        nearestNeighbor = NearestNeighbor(self)
        nearestNeighbor.simple_nearestNeighborHeuristic()
        savingHeuristic = SavingHeuristic(self)
        savingHeuristic.simpleSaving()

        self.printPerformance("Greedy Simple Version",nearestNeighbor,savingHeuristic)
        nearestNeighbor.random_nearestNeighborHeuristic(10)
        savingHeuristic.randomSaving(10)
        self.printPerformance("Greedy Randomized Version",nearestNeighbor,savingHeuristic)

        twoOpt = TwoOpt(self,nearestNeighbor.SolutionPaths , savingHeuristic.SolutionPaths)
        twoOpt.firstImprove()
        self.printPerformance2("2-opt results for first improvement",twoOpt)
        twoOpt.bestImprove()
        self.printPerformance2("2-opt results for best improvement", twoOpt)

        self.printComparison(twoOpt)


    def printPerformance2(self,whichHeuristic,twoOpt):
        print()
        print("---------", whichHeuristic, "----------")
        firstTab = 8
        print("\t\t\t\tAvg Case %s|   Best Case %s|    Worst Case"%("\t"*firstTab, "\t"*firstTab))
        print("-"*250)
        print("NH ->\t\t\t  ", twoOpt.neighborAvgCost," \t\t\t\t\t|",twoOpt.neighborBestCost," \t\t\t\t\t\t|",twoOpt.neighborWorstCost)
        print("SH ->\t\t\t  ", twoOpt.savingAvgCost," \t\t\t\t\t|",twoOpt.savingBestCost," \t\t\t\t\t\t|",twoOpt.savingWorstCost)

    def printComparison(self,twoOpt):
        print()
        print("---------", "Performance Compare", "----------")
        firstTab = 8
        actualCost =  Constant.bestCost[self.whichInput]
        bestCost = twoOpt.bestInBestImprove
        firstCost = twoOpt.bestInFirstImprove

        print("Optimal Cost ->" ,actualCost," 100%")
        print("First Improve ->",firstCost," ",firstCost / actualCost * 100 ,"%")
        print("Best Improve ->",bestCost," ",bestCost / actualCost * 100 ,"%")

    def takeInput(self, lineList):
        for line in lineList:
            tmpRow = [float(p) for p in line.split()]
            self.pointList.append(Node(tmpRow[0], tmpRow[1]))

    # Given a node X, following function returns the k nearest unvisited nodes of X
    def getK_ClosestUnvisitedNodeOf(self, curnNodeIndx, k):
        tmpLst = []
        for j in range(0, self.n):
            if self.vis[j] or j == curnNodeIndx:
                continue
            tmpLst.append(j)
        tmpLst.sort(key=lambda x:self.adjMat[curnNodeIndx][x])
        return tmpLst[0:min(len(tmpLst),k)]

    def buildAdjMatrix(self):
        for i in range(0, self.n):
            self.adjMat[i][i] = 0
            for j in range(i + 1, self.n):
                self.adjMat[i][j] = self.adjMat[j][i] = self.pointList[i].getDistanceBetween(self.pointList[j])

    def costBetween(self, node1Indx, node2Indx):
        return self.adjMat[node1Indx][node2Indx]




