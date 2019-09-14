# File: ROB 456, Assignment 4
# Author: Kenzie Brian
# Date: November 2017
# Description: For ROB 456. Runs A* search algorithm on world.csv to find best path.
 
import numpy as np
import Queue as Q
import csv
import time
 
 
#Helpful Class for graph node YAY
class graphNode(object):
    # Pointers to edges
    #              N     E     S     W
    connections = [None, None, None, None]
 
    heur = -1
    parent = None
    parentDir = -1;
    location = np.array([0,0])
 
    def __init__(self, parent, loc):
        self.parent = parent
        self.location = loc
 
    def setEdges(self, edgeList):
        self.connections = edgeList
 
    def setHeur(self, heur):
        self.heur = heur
 
    def getLoc(self):
        return self.location
 
    def getHeur(self):
        return self.heur
 
    def getEdges(self):
        return self.connections
 
    def getIndex(self):
        return self.location[0]*20 + self.location[1]


 
#Helpful Functions YAY
 
#Reset traversal flags for print
def clearTravFlags(cellMap):
    for row in range(len(cellMap)):
        for col in range(len(cellMap[row])):
            if cellMap[row][col][0] == 2:
                cellMap[row][col][0] = 0;


 
#Searches the connections at a point, creates node objects for cells not yet seen
def getNodes(location, cellMap):
     
    #       N      E     S     W
    nodes = [None, None, None, None]
     
    #Check direction of connections
    for i in range(0, 4):
 
        row = location[0]
        col = location[1]
 
        if i==0:   # North
            row = row-1
        elif i==1: # East
            col = col+1
        elif i==2: # South
            row = row+1
        elif i==3: # West
            col = col-1

        #index for out-of-bounds (ie not in matrix)
        if (row>=0 and col>=0 and row<cellMap.shape[0] and col<cellMap.shape[1]):
            #if cell is unobstructed and undiscovered
            if (cellMap[row, col, 0] == 0):
                # new cell
                cellMap[row, col, 0] = 2; # Add discovered flag
                #new graphNode object
                nodes[i] = graphNode(None, [row, col])
                cellMap[row, col, 1] = nodes[i]
 
            #Cell has been discovered, not new, ues existing ptr
            elif (cellMap[row, col, 0] == 2):
                nodes[i] = cellMap[row, col, 1] 
    return nodes
 
 
 
#Reads csv file and creates a matrix of tuples with size of the csv
#Tuples: (mapDigit, pointer to graphNode object)
def readCSVFromPath(path, permissions, delim):
     
    #Read the CSV
    with open(path, permissions) as csvfile:
        mtx = list(csv.reader(csvfile, delimiter=delim))
     
    #list of lists of chars to array of arrays of ints
    for row in range(len(mtx)):
        for cell in range(len(mtx[row])):
            #char to (integer, node-pointer) tuple
            mtx[row][cell] = [int(mtx[row][cell]), None]
        #cols in row
 
        #list to array   
        mtx[row] = np.array(mtx[row])
    #rows in mtx
 
    #list of arrays to array of arrays
    mtx = np.array(mtx)
 
    return mtx
 
 
 
#Cellmap as graph
#Assumes head is at [0,0]
def generateGraphFromMap(cellMap):
 
    #rows
    for row in range(0, len(cellMap)):
 
        #columns in row
        for cell in range(0, len(cellMap[row])):
 
            #map[cell] == 1 -> cell unreachable
            if cellMap[row, cell, 0] != 1:
                 
                # map[cell] == 0 -> cell undiscovered; make
                if cellMap[row, cell, 0] == 0:
                    cellMap[row, cell, 0] = 2
                    cellMap[row, cell, 1] = graphNode(None, [row, cell])
                # end undiscovered
 
                cellMap[row, cell, 1].setEdges(getNodes([row, cell], cellMap))
        #cols in row
    #rows in mtx
 
 
 
#clac heur for all
def estimateHeuristicForGraph(cellMap, goal):
     
    for row in range(len(cellMap)):
        for cell in range(len(cellMap[row])):
            node = cellMap[row][cell][1]
            if node != None: node.setHeur(abs(node.getLoc()[0]-goal[0]) + abs(node.getLoc()[1]-goal[1]))		#calc heur


 
 
#from Queue.PriorityQueue to add tuple[1].contains([value]) functionality
class ExQ(Q.PriorityQueue):
 
    # This data structure assumes the following format:
    # (priority, value, value), where the values are implemented as
    # (distanceToGoal, [row, col], [parentRow parentCol])
     
    #Return bool if queue contains a value
    def contains(self, value):
        if not self.empty():
            return value in (i[1] for i in self.queue)
        else:
            return 0
 
    #Show lowest priority item
    def peek(self):
        if not self.empty():
            temp = self.get()
            self.put(temp)
            return temp
        else:
            return None
 
    #Returns priority of item in list
    #assumes no duplicates in queue
    def priority(self,value):
        for i in self.queue:
            if i[1] == value:
                return i[0]
        return None
 
    #Resets priority of the first matching value
    #Assumes no duplicates in queue
    def replace(self, (priority, value)):
        for i in self.queue:
            if i[1] == value:
                i[0] = priority
                return 1
        return 0
 
     
    def parentOf(self, value):
        for i in self.queue:
            if i[1] == value:
                return i[2]     
        return None
 
 
#ACTUAL ALGORTIHM
#Assumes the following global variables exist
#edgeCosts := matrix of edge costs; cost from a to b is edgeCost[a_row][a_col][direction to b] 
#cellMap := map of nodes structured in 20x20; see graphNode object in charGrid.py
#openSet := priority queue of open nodes
#closedSet := priorirty queue of closed nodes
def A_Star():
    global edgeCosts
    global cellMap
    global openSet
    global closedSet
 
    #Recursive ish end case
    if openSet.empty():
        return
     
    #local copies
    (estDist, localIndex, parentIndex) = openSet.get()
 
    #object that contains all node info
    cell = getCellInMap(localIndex)
    parent = getCellInMap(parentIndex)
     
    #Get [row][col] index of the node
    (row, col) = cell.getLoc()
     
    #local copy
    localCost = estDist - cell.getHeur() 
     
    # Take from front of OQ and add to CQ
    closedSet.put( (localCost, localIndex, parentIndex) )
 
    #accesses edge costs
    count = 0;
    localEdgeCosts = edgeCosts[row][col][:]
 
    #Edges are node objects at connections
    for edge in cell.getEdges():
 
        #check dir if connected
        if edge != None:
             
            #local copy
            index = edge.getIndex()
             
            #Don't check cells if in CQ
            if not closedSet.contains(index):
                 
                #cost + heuristic at loc
                localEdgeCosts[count] = localEdgeCosts[count] + edge.getHeur();
                 
                #compare or add
                if openSet.contains(index):
 
                    #compare distance with goal
                    if (localCost+localEdgeCosts[count]) < openSet.priority(index):
 
                        #replace if better
                        openSet.replace((localCost+localEdgeCosts[count], index, localIndex))
                else:
                    #new in queue if unseen
                    openSet.put((localCost + localEdgeCosts[count], index, localIndex))
            else:
                #unwanted case detection
                localEdgeCosts[count] = -1;
        else:
            #unwanted case detection
            localEdgeCosts[count] = -1;
 
        #Keeps track of direction
        count = count+1
    A_Star()
 
 
 
#returns the graphNode object at index
def getCellInMap(ind):
    global cellMap
    col = ind % 20;
    row = (ind-col)/20
    return cellMap[row][col][1]
 
 
 
#Prints the final path to the screen
def printPath(path):
 
    #Clear map for printing
    clearTravFlags(cellMap)
 
    #Init a blank character matrix for printing
    charMap = [[' ' for c in range(20)] for r in range(20)]
     
    #path on the global grid
    for index in path:
        node = getCellInMap(index).getLoc()
        #print node
        (row, col) = node
        print(row,col)
        cellMap[row][col][0] = 2
     
    #grid into char mtx
    for row in range(len(cellMap)):
        for col in range(len(cellMap[row])):
            cell = cellMap[row][col][0]
            if cell == 1:
                charMap[row][col] = '1'
            elif cell == 2:
                charMap[row][col] = '.'
            else:
                charMap[row][col] = '0'
     
    # Print the char mtx
    for row in charMap:
        print ''.join(row)

 
 
def generatePathFromCQ(endLoc):
     
    global cellMap
 
    cell = cellMap[endLoc[0]][endLoc[1]][1]
    path = []
    path.append(cell.getIndex())
    parent = getCellInMap(closedSet.parentOf(cell.getIndex()))
    distance = closedSet.priority(cell.getIndex())
    while parent is not cell:
        cell = parent
        parentIndex = closedSet.parentOf(cell.getIndex())
        parent = getCellInMap(parentIndex)
        path.append(cell.getIndex())
    return (path, distance)
 
 
#MAINNNNNNN
#Global variables but only for main
edgeCosts = [[[1, 1, 1, 1] for cell in range(20)] for row in range(20)] 
cellMap = readCSVFromPath('world.csv', 'rU', ',')
openSet = ExQ()
closedSet = ExQ()
world = []
if __name__ == "__main__":
  
    edgeCosts = [ [[1, 1, 1, 1] for cell in range(20) ] for row in range(20)] 
    cellMap = readCSVFromPath('world.csv', 'rU', ',')
    openSet = ExQ()
    closedSet = ExQ()
 
    #Define start and end locations on map
    startLoc = np.array([0,0])
    endLoc = np.array([19,19])
 
    #matrix to undirected graph
    generateGraphFromMap(cellMap)
    #Sets start location for graph
    graphHead = cellMap[startLoc[0],startLoc[0],1]
    #Iterate through entire matrix of cells to set heuristic
    estimateHeuristicForGraph(cellMap, endLoc)
    #Starts node
    openSet.put( (graphHead.getHeur(), graphHead.getIndex(), graphHead.getIndex()) )
 
    #Does the stuff
    A_Star()
 
    #Get path from the closed queue from astar
    (path, distance) = generatePathFromCQ(endLoc)
    #Print path
    printPath(path)
    print 'AStar Path Distance:', distance, 'cells'

 
