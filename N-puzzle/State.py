import math
from Constant import Constant


class State:

    def __init__(self, n):
        self.n = n
        self.dimension = int(math.sqrt(n + 1))
        self.ara = []
        self.emptyCell = (self.dimension, self.dimension)
        self.cost = 0
        self.heuristicCost = 0
        self.heuristic = ""
        self.parent = None

    def setStateAfterSwap(self, state, curCell, neighborCell):
        for row in state.ara:
            self.ara.append(list(row))
        self.ara[curCell[0]][curCell[1]], self.ara[neighborCell[0]][neighborCell[1]] = self.ara[neighborCell[0]][
                                                                                           neighborCell[1]], \
                                                                                       self.ara[curCell[0]][curCell[1]]
        self.cost = state.cost + 1
        self.setHeuristic(state.heuristic)
        self.emptyCell = neighborCell

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic
        if heuristic.lower().find(Constant.HammingHeuristic) != -1:
            self.heuristicCost += self.getHammingDistance()
        elif heuristic.lower().find(Constant.LinearHeuristic) != -1:
            self.heuristicCost += self.getLinearConflict()
        elif heuristic.lower().find(Constant.ManhattanHeuristic) != -1:
            self.heuristicCost += self.getManhattanDistance()

    def takeInput(self, lineList):
        tmpRow = [0, 0]
        self.ara.append(tmpRow)
        i = 1
        for line in lineList:
            tmpRow = [int(p) for p in line.split()]
            for j in range(len(lineList)):
                if tmpRow[j] == Constant.Blank: self.emptyCell = (i, j + 1)
            tmpRow[1:self.dimension + 1] = tmpRow
            self.ara.insert(i + 1, tmpRow)
            i += 1

    def isValidCell(self, cell):
        return (1 <= cell[0] <= self.dimension) and (1 <= cell[1] <= self.dimension)

    def isGoalState(self):
        return self.heuristicCost == 0

    def isSolvable(self):
        lst = []
        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                if self.ara[i][j] == Constant.Blank: continue
                lst.append(self.ara[i][j])
        inversion = 0

        for i in range(len(lst)):
            for j in range(i+1, len(lst)):
                if lst[i] > lst[j]:
                    inversion += 1

        if self.dimension % 2 ==1:
            return not (inversion % 2 == 1)
        else:
            return (inversion + self.emptyCell[0]-1) % 2 == 1

    def getNeighbourList(self):
        neighborList = list()
        for i in range(len(Constant.move)):
            adCell = list(map(lambda x, y: x + y, self.emptyCell, Constant.move[i]))
            if self.isValidCell(adCell):
                neighborState = State(self.n)
                neighborState.setStateAfterSwap(self, self.emptyCell, adCell)
                neighborState.parent = self
                neighborList.append(neighborState)
        return neighborList

    def getHammingDistance(self):
        match = 1
        cnt = 0
        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                if self.ara[i][j] == Constant.Blank: match +=1 ; continue
                if self.ara[i][j] != match:
                    cnt += 1
                match += 1
        return cnt

    def getCorrectCellFor(self, number):
        return int(math.ceil(number / self.dimension)), self.dimension if number % self.dimension == 0 else number % self.dimension

    def getManhattanDistance(self):
        cnt = 0
        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                if self.ara[i][j] == Constant.Blank: continue
                (row, col) = self.getCorrectCellFor(self.ara[i][j])
                cnt += abs(row - i) + abs(col - j)

        return cnt

    def getLinearConflict(self):
        linConflict = 0
        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                if self.ara[i][j] == Constant.Blank: continue
                number = self.ara[i][j]
                cell = self.getCorrectCellFor(number)
                if (i, j) == cell: continue  # if Correct Cell
                if i == cell[0]:  # if correct row
                    for fromCol in range(j + 1, self.dimension + 1):
                        if number > self.ara[i][fromCol]:
                            linConflict += 1
                elif j == cell[1]:  # if correct column
                    for fromRow in range(i + 1, self.dimension + 1):
                        if number > self.ara[fromRow][j]:
                            linConflict += 1

        return self.getManhattanDistance() + 2 * linConflict

    def __str__(self):
        string = ""
        for i in range(1, self.dimension + 1):
            for j in range(1, self.dimension + 1):
                string += str(self.ara[i][j]) + " "
            string += "\n"
        return string

    def __eq__(self, other):
        return self.ara == other.ara

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash(tuple([tuple(i) for i in self.ara]))