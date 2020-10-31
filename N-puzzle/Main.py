from StateSpace import StateSpace
from Constant import Constant


file = open("input.txt", "r")
isFirstLine = True
state = None
lineList = []
for line in file:
    if isFirstLine:
        state = StateSpace(int(line))
        isFirstLine = False
    else:
        lineList.append(line.strip())
state.input(lineList)

print("Enter which heuristic to run: ")
print("1 - Linear Conflict heuristic")
print("2 - Manhattan distance heuristic")
print("3 - Hamming distance heuristic ")
choice = int(input())

if choice == 1:
    state.AstarSearch(Constant.LinearHeuristic)
elif choice == 2:
    state.AstarSearch(Constant.ManhattanHeuristic)
elif choice ==3:
    state.AstarSearch(Constant.HammingHeuristic)
