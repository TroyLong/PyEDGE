########################
##        About       ##
########################
# These are a series of tests for neighbor finding.
# Split from neighborAnalysis.py because they are dealing with the data in completely different ways
# TODO:: RUN SPEED TESTS
########################
## Imported Libraries ##
########################
from copy import deepcopy
import dataTypes.cell as ce
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT
from dataTypes.dataTypeTraits import imageStateTraits as iST


#TODO:: Deepcopy might be too slow
#Functional Form, might require deepcopy to work properly though
def distanceFilter(state,deviation):
    tempCells = deepcopy(state[iST.CELLS])
    for cell in tempCells:
        cellularDistanceFilter(cell,deviation)
    return tuple(tempCells)

# Is not functional, since it removes from cell and cell neighbor
# If it is passed a copy, it is effectivily functional
def cellularDistanceFilter(cell,deviation):
    cell[cT.NEIGHBORS] = ce.sortNeighbors(cell)
    # this is the furthest distance to allowed neighbor. Starts at the shortest
    maxDistance = cell[cT.NEIGHBORS][0][cNT.DISTANCE_TO_BORDER] if (len(cell[cT.NEIGHBORS]) > 0) else 0
    # Bypasses isWithinAllowedDistance() computation after it fails the first time
    pastAllowed = False
    for possibleNeighbor in cell[cT.NEIGHBORS]:
        # possibly faster to nest, but not as clean
        if (not pastAllowed) and (isWithinAllowedDistance(cell,possibleNeighbor,maxDistance,deviation)): 
            maxDistance = possibleNeighbor[cNT.DISTANCE_TO_BORDER]
        else:
            pastAllowed = True
        if pastAllowed:
            cell[cT.NEIGHBORS],possibleNeighbor[cNT.CELL][cT.NEIGHBORS] = ce.removeNeighborTwoWay(cell,possibleNeighbor)


#TODO:: This is messy, and both booleans are probably not neccessary
# checks if neighbor is within the limit on distances past the current maxDistance
def isWithinAllowedDistance(cell, possibleNeighbor, maxDistance,deviation):
    distLimit = 1.75*(cell[cT.RADIUS] + possibleNeighbor[cNT.CELL][cT.RADIUS])
    neighborInDistLimit = possibleNeighbor[cNT.DISTANCE_TO_BORDER] < distLimit
    neighborInDevationLimit = possibleNeighbor[cNT.DISTANCE_TO_BORDER] < maxDistance+deviation
    return neighborInDistLimit and neighborInDevationLimit