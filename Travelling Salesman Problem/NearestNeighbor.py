from random import randint

from Constant import *
from SolutionPath import Solution


class NearestNeighbor:

    def __init__(self,graph):
        self.graph = graph
        self.vis = [False] * graph.n

        self.simpleBestSrc = 0
        self.SolutionPaths = []

        self.avgCost = 0
        self.bestCost = Constant.INF
        self.worstCost = 0

    def simple_nearestNeighborHeuristic(self):
        self.avgCost = 0
        self.bestCost = Constant.INF
        self.worstCost = 0

        totalCost = 0

        for k in range(0,self.graph.n):
            curNodeIndx = k
            neighborIndx = 0
            visCnt = 0
            self.graph.vis = [False] * self.graph.n
            solutionPath = Solution(self.graph)

            while visCnt != self.graph.n:
                self.graph.vis[curNodeIndx] = True
                solutionPath.append(curNodeIndx)
                try:
                    neighborIndx = self.graph.getK_ClosestUnvisitedNodeOf(curNodeIndx, 1)[0]
                except:
                    x = 1
                curNodeIndx = neighborIndx
                visCnt += 1

            pathCost = solutionPath.getCostOfTour()
            totalCost += pathCost

            if pathCost < self.bestCost:
                self.bestCost, self.simpleBestSrc = pathCost, k
            self.worstCost = max(self.worstCost, pathCost)

            solutionPath.insertIntoBest1(self.SolutionPaths, solutionPath)

        self.avgCost = totalCost / self.graph.n

    def random_nearestNeighborHeuristic(self, iterationNum):
        self.avgCost = 0
        self.bestCost = Constant.INF
        self.worstCost = 0

        totalCost = 0
        for k in range(0, iterationNum):
            curNodeIndx = self.simpleBestSrc
            neighborIndx = 0
            visCnt = 0
            self.graph.vis = [False] * self.graph.n
            solutionPath = Solution(self.graph)

            while visCnt != self.graph.n:
                if self.graph.vis[curNodeIndx]: continue
                self.graph.vis[curNodeIndx] = True
                solutionPath.append(curNodeIndx)
                try:
                    neighborList = self.graph.getK_ClosestUnvisitedNodeOf(curNodeIndx, 5)
                    neighborIndx = neighborList[randint(0, len(neighborList)-1)]
                except:
                    x = 1
                curNodeIndx = neighborIndx
                visCnt += 1

            pathCost = solutionPath.getCostOfTour()
            totalCost += pathCost

            self.bestCost = min(self.bestCost, pathCost)
            self.worstCost = max(self.worstCost, pathCost)
            solutionPath.insertIntoBest4(self.SolutionPaths, solutionPath)

        self.avgCost = totalCost / iterationNum


