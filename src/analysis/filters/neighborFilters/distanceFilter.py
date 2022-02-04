########################
##        About       ##
########################
# These are a series of tests for neighbor finding.
# Split from neighborAnalysis.py because they are dealing with the data in completely different ways

########################
## Imported Libraries ##
########################
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT
from dataTypes.dataTypeTraits import imageStateTraits as iST

#TODO:: Incorperate cell.py removal
# Functional Form
# Takes neighbors out of the neighbor list if they are 
def distanceFilter(state,deviation):
    tempCells = list()
    for cell in state[iST.CELLS]:
        tempCells.append(cellularDistanceFilter(cell,deviation))
    return tuple(tempCells)


#TODO:: To make this better, I should first sort the neighbors somewhere else, perhaps under a clean data function
def cellularDistanceFilter(cell,deviation):
    # sorts neighbors by distance
    sortedNeighbors = sorted(cell[cT.NEIGHBORS], key=lambda cellN: cellN[cNT.DISTANCE_TO_BORDER])    
    realNeighbors = list()
    # returned cell datastructure. Does not alter the original cell
    tempCell = cell.copy()
    maxDistance = 0
    if len(cell[cT.NEIGHBORS]) > 0:
        # this is the furthest distance to allowed neighbor. Starts at the shortest
        maxDistance = cell[cT.NEIGHBORS][0][cNT.DISTANCE_TO_BORDER]
    for possibleNeighbor in sortedNeighbors:
        if isWithinAllowedDistance(cell,possibleNeighbor,maxDistance,deviation):
            # if neighbor is in limit, adds it to final neighbor list
            realNeighbors.append(possibleNeighbor)
        else:
            # the list is sorted, and no others will be successful
            break
        # set new max distance
        maxDistance = possibleNeighbor[cNT.DISTANCE_TO_BORDER]
    tempCell[cT.NEIGHBORS] = realNeighbors
    # sets the neighbor list to be the new one based on the filter
    # DO NOT CHANGE TO TUPLE ON ACCIDENT
    return tempCell


#TODO:: This is messy, and both booleans are probably not neccessary
# checks if neighbor is within the limit on distances past the current maxDistance
def isWithinAllowedDistance(cell, possibleNeighbor, maxDistance,deviation):
    distLimit = 1.75*(cell[cT.RADIUS] + possibleNeighbor[cNT.CELL][cT.RADIUS])
    neighborInDistLimit = possibleNeighbor[cNT.DISTANCE_TO_BORDER] < distLimit
    neighborInDevationLimit = possibleNeighbor[cNT.DISTANCE_TO_BORDER] < maxDistance+deviation
    return neighborInDistLimit and neighborInDevationLimit