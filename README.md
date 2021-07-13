# A* Pathfinding

<div align="center">

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fjlsuh%2Fa-star-pathfinding&count_bg=%2379C83D&title_bg=%23555555&icon=spacex.svg&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>

## Description
A* is a modification of Dijkstra’s Algorithm that is optimized for a single destination. Dijkstra’s Algorithm can find paths to all locations, while A* finds paths to one location or the closest of several locations. It prioritizes paths that seem to be leading closer to a goal.

## Built With
- [Brython 3.9.5](https://brython.info/)

## How it Works
The key feature of the A* algorithm is that it keeps a track of each visited node, which helps ignoring already visited nodes. It also has a list that holds all the nodes that are left to be explored and from this list chooses the most optimal node saving a huge amount of time (not exploring unnecessary or less optimal nodes).

There are two lists namely `open list` and `closed list`:
- Open list: contains all the nodes that are being generated and are not contained in the closed list.
- Closed list: contains all the nodes explored after its neighboring nodes are discovered. Its neighbors are put in the open list.

Each node holds a pointer to its parent, retracing the path to the parent node at any given time. Initially, the open list holds the start node. The next node is chosen from the open list based on its `f cost`: node with the least f cost is picked up and explored.

### What is F Cost?
f cost is nothing but the sum of the cost to reach that node from start (initial node) and the heuristic value of that node.

For any give node f score is defined as:
<div align="center">
    <img src="https://latex.codecogs.com/png.image?\dpi{150}&space;\bg_white&space;f(x)&space;=&space;g(x)&space;&plus;&space;h(x)" title="\bg_white f(x) = g(x) + h(x)" />
</div>

where `g(x)` is the cost of that node relative to the initial node, while `h(x)` is the calculated heuristic of that node.

### What is G Cost?
`g cost` is defined as the sum of the parent's g cost and the cost of travelling to that node from its parent:

<div align="center">
    <img src="https://latex.codecogs.com/png.image?\dpi{150}&space;\bg_white&space;g(x)&space;=&space;g(x.parent)&space;&plus;&space;cost(x.parent,&space;x)" title="\bg_white g(x) = g(x.parent) + cost(x.parent, x)" />
</div>

### What is H Cost (heuristic)?
Heuristic needs to be admissible for each type of problem. To simplify the given implementaiton `h cost` was defined as the manhattan distance from the current node to the objetive node:

<div align="center">
    <img src="https://latex.codecogs.com/png.image?\dpi{150}&space;\bg_white&space;h(x)&space;=&space;|start.x&space;-&space;objective.x|&space;&plus;&space;|start.y&space;-&space;objective.y|" title="\bg_white h(x) = |start.x - objective.x| + |start.y - objective.y|" />
</div>

## Usage Controls
Node creation:
- Start Node: place starting point.
- End Node: place objective.
- Wall Node: create wall nodes (blockage).

Node restoring:
- Restore Node: restore a single node.
- Restore Map: restore current execution (nodes' state are preserved).
- New Map: start from scratch.

Algorithm Execution:
- Start Pathfind: executes algorithm (spacebar can be used as an alternative way).

## TODO List
- [ ] Range slider to set map dimentions
- [ ] Considering diagonal movements
- [ ] Map uploader through .txt files
- [ ] Describe button usages
- [ ] Variable speed execution (step by step preview)
- [x] Button for pathfinding execution
- [ ] Improve readme
- [ ] Refactors

## References
- A [Java implementation](https://www.youtube.com/watch?v=1-YPj5Vt0oQ) by [Devon Crawford](https://github.com/DevonCrawford)
- [Amit's A* Pages](https://theory.stanford.edu/~amitp/GameProgramming/) by Red Blob Games
- [Definition of heuristic](https://en.wikipedia.org/wiki/Heuristic_(computer_science))