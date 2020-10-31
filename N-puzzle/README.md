[N-puzzle](https://en.wikipedia.org/wiki/15_puzzle) is one of well-known classical problems for modelling alogirtm using heuristic.

Gist of problem description is as follows :
```
Given a k x k grid with k<sup>2</sup>-1 (=n) square blocks labeled 1 through n and a blank square. 
Our goal is to rearrange the blocks so that they are in order, using as few moves as possible.
A move can be either a horizontal or vertical sliding of block 
```

We have used A* search to solve this problem idea of which is pretty similar **Dijkstra Algorithm** except this algorithm uses heuristic. The success of this approach largely depends on the choice of heuristic.

We have considered three heuristic

* **Hamming Distance** : The number of blocks in the wrong position (excluding the blank)
* **Manhattan distance**: The sum of the Manhattan distances (sum of the vertical and
horizontal distance) from the blocks to their goal positions.
* **Linear Conflict**: Two tiles t<sub>j</sub> and t<sub>k</sub> are in a linear conflict if t<sub>j</sub> and t<sub>k</sub> are the same line, the
goal positions of t<sub>j</sub> and t<sub>k</sub> are both in that line,t<sub>j</sub> is to the right of t<sub>k</sub> , and goal position of t<sub>j</sub>
is to the left of the goal position of t<sub>k</sub> . Here line indicated both rows and columns. The
linear conflict heuristic is calculated as Manhattan distance + 2*(Linear conflicts).

Process to run the Project:

**Step 1**:

    Put the input board configuration in input.txt file.
    Input format:
    
    Line 1 : Number of tiles on the board k<sup>2</sup>-1 (=n)
    Next put initial k X k board configuration with -1 denoting blank
    
**Step 2**:

    Run Main.py

    
    
