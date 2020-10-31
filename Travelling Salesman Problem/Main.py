from Graph import Graph
from Constant import Constant

# 0 -> pr76
# 1 -> berlin52
# 2 -> st70
whichInput = 1
pr76 = 0
berlin52 = 1
st70 = 2
print("Chose Input File")
print("0 for pr76")
print("1 for berlin52")
print("2 for st70")
filChoice = int(input())
file = open(Constant.files[filChoice], "r")
isFirstLine = True
graph = None
lineList = []
for line in file:
    if isFirstLine:
        graph = Graph(int(line), filChoice)
        isFirstLine = False
    else:
        lineList.append(line.strip())

graph.takeInput(lineList)
graph.buildAdjMatrix()
print("-------------",Constant.files[filChoice],"-----------------------")
graph.runHeuristic()
