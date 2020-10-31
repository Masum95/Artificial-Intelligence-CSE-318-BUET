
from State import State
import heapq
import timeit


class StateSpace:

    def __init__(self, n):
        self.startState = State(n)
        self.runTime = {}

    def input(self,lineList):
        self.startState.takeInput(lineList)

    def printSolutionSteps(self,state):
        stack = []
        curNode = state
        while(curNode is not None):
            stack.append(curNode)
            curNode = curNode.parent

        while stack:
            curNode = stack.pop()
            print(curNode, " -> "),
        print("Number of moves to reach Goal state = ",curNode.cost)

    def AstarSearch(self,heuristic):
        dist =  {}
        start = timeit.default_timer()
        self.startState.setHeuristic(heuristic)
        pq = []
        dist[self.startState] = 0
        heapq.heappush(pq, (0, self.startState))
        visited = set()
        solvable = False
        curNode = None
        exploredNode = 0
        expandedNode = 0
        while pq:

            curNode = heapq.heappop(pq)[1]

            if curNode.isGoalState():
                solvable = True
                break
            expandedNode += 1
            lst = curNode.getNeighbourList()
            for t in lst:
                if not t.isSolvable():
                    continue

                if t not in dist or t.cost + t.heuristicCost < dist[t]:
                    dist[t] = t.cost + t.heuristicCost
                    heapq.heappush(pq, (t.cost + t.heuristicCost, t))
                    exploredNode += 1

        end = timeit.default_timer()
        self.runTime[heuristic] = end - start
        if solvable:
            self.printSolutionSteps(curNode)
        else:
            print("Can't solve this board configuration")
        print("Total number of explored node : ", exploredNode)
        print("Total numbe of expanded node :", expandedNode)
        print("Total Execution time in ",heuristic, ":  ",str(end-start), "s")





