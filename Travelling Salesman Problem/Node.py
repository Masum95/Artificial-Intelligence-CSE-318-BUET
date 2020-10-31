import math


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getDistanceBetween(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __str__(self):
        return "(" + str(self.x) + ", " +str(self.y)  +")"

