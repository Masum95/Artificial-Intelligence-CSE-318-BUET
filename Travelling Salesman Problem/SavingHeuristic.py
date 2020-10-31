from random import randint
import random
from Constant import *
from SolutionPath import Solution


class SavingHeuristic:

    def __init__(self,graph):
        self.graph = graph
        self.parents = [0]*graph.n

        self.simpleBestSrc = 0
        self.SolutionPaths = []

        self.avgCost = 0
        self.bestCost = Constant.INF
        self.worstCost = 0
        self.savingList = []

    def simpleSaving(self):
        self.avgCost = 0
        self.bestCost = Constant.INF
        self.worstCost = 0

        totalCost = 0

        n = self.graph.n
        for k in range(0, self.graph.n):
            src = k

            adjMat = [[Constant.INF for x in range(n)] for y in range(n)]
            for i in range(n):
                adjMat[i][src] = adjMat[src][i] = self.graph.costBetween(src, i)
            for i in range(n):
                self.parents[i] = i

            savingList = self.getSavingListWithSrc(src)
            solutionPath = Solution(self.graph)

            mergeCnt = 0
            for savingEntity in savingList:
                if self.mergeIfPossible(savingEntity.x, savingEntity.y, src, adjMat):
                    mergeCnt += 1
                if mergeCnt == n-2:
                    break

            vis = [False] * n
            vis[src] = True
            visCnt = 0
            curNode = src
            while visCnt != n:
                solutionPath.append(curNode)
                visCnt += 1
                for i in range(n):
                    if (adjMat[curNode][i] != Constant.INF or adjMat[i][curNode] != Constant.INF) and not vis[i]:
                        vis[i] = True
                        curNode = i
                        break
            pathCost = solutionPath.getCostOfTour()
            totalCost += pathCost

            if pathCost < self.bestCost:
                self.bestCost, self.simpleBestSrc = pathCost, k
            self.worstCost = max(self.worstCost, pathCost)

            solutionPath.insertIntoBest1(self.SolutionPaths, solutionPath)

        self.avgCost = totalCost / self.graph.n

    def randomSaving(self,iterationNum):
        self.avgCost = 0
        self.bestCost = Constant.INF
        self.worstCost = 0
        
        totalCost = 0

        n = self.graph.n
        src = self.simpleBestSrc
        savingList = self.getSavingListWithSrc(src)
        for k in range(iterationNum):
            adjMat = [[Constant.INF for x in range(n)] for y in range(n)]
            for i in range(n):
                adjMat[i][src] = adjMat[src][i] = self.graph.costBetween(src, i)
            for i in range(n):
                self.parents[i] = i

            solutionPath = Solution(self.graph)

            mergeCnt = 0
            for i in range(0, len(savingList)):
                indx = randint(i, min(i+4, len(savingList)-1))
                savingEntity = savingList[indx]

                if self.mergeIfPossible(savingEntity.x, savingEntity.y, src, adjMat):
                    mergeCnt += 1
                if mergeCnt == n - 2:
                    break
                savingList[i], savingList[indx] = savingList[indx], savingList[i]

            vis = [False] * n
            vis[src] = True
            visCnt = 0
            curNode = src

            while visCnt != n:
                solutionPath.append(curNode)
                visCnt += 1
                for i in range(n):
                    if adjMat[curNode][i] != Constant.INF and not vis[i]:
                        vis[i] = True
                        curNode = i
                        solutionPath.append(i)
                        break

            pathCost = solutionPath.getCostOfTour()
            totalCost += pathCost

            if pathCost < self.bestCost:
                self.bestCost = pathCost
            self.worstCost = max(self.worstCost, pathCost)
            solutionPath.insertIntoBest4(self.SolutionPaths, solutionPath)
        self.avgCost = totalCost / iterationNum

    def getKBestSavingList(self,prevList,k):
        cnt = [0]*self.graph.n
        retList = []
        for entity in prevList:
            if cnt[entity.x] <=k:
                cnt[entity.x] += 1
                retList.append(entity)
        random.shuffle(retList)
        return retList

    # returns saving list in descending order of saving cost
    def getSavingListWithSrc(self,src):
        lst = []
        for i in range(0,self.graph.n):
            if i == src: continue
            for j in range(i+1,self.graph.n):
                if j == src: continue
                lst.append(self.savingEntity(i, j, self.graph.costBetween(i, src) + self.graph.costBetween(j, src) - self.graph.costBetween(i, j)))

        lst.sort(key=lambda x: x.savingCost, reverse=True)
        return lst

    def canBeMerged(self,x,y,src,adjMat):
        return (adjMat[x][src] != Constant.INF or adjMat[src][x] != Constant.INF ) and (adjMat[y][src] != Constant.INF or adjMat[src][y] != Constant.INF ) and self.parents[x] != self.parents[y]

    def mergeIfPossible(self,x, y, src, adjMat):
        if not self.canBeMerged(x,y,src,adjMat): return False

        if adjMat[x][src] != Constant.INF:
            adjMat[x][src] = Constant.INF
        elif adjMat[src][x] != Constant.INF:
            adjMat[src][x] = Constant.INF

        if adjMat[y][src] != Constant.INF:
            adjMat[y][src] = Constant.INF
        elif adjMat[src][y] != Constant.INF:
            adjMat[src][y] = Constant.INF

        if self.parents[x] < self.parents[y]:
            head = self.parents[y]

            for i in range(self.graph.n):
                if self.parents[i] == head:
                    self.parents[i] = self.parents[x]
        elif self.parents[y] < self.parents[x]:
            head = self.parents[x]
            for i in range(self.graph.n):

                if self.parents[i] == head:
                    self.parents[i] = self.parents[y]

        adjMat[x][y] = adjMat[y][x] = self.graph.costBetween(x,y)
        return True

    class savingEntity:

        def __init__(self, x, y, savingCost):
            self.x = x
            self.y = y
            self.savingCost = savingCost

        def __str__(self) -> str:
            return str(self.x) + " " + str(self.y) + " " + str(self.savingCost)




