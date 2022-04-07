########################
##        About       ##
########################
# These are a series of tests for neighbor finding.
# Split from neighborAnalysis.py because they are dealing with the data in completely different ways
# TODO:: RUN SPEED TESTS
########################
## Imported Libraries ##
########################
import copy
import dataTypes.cell as ce

#TODO:: Deepcopy might be too slow
#Functional Form, might require deepcopy to work properly though
def distanceFilter(state,deviation):
    temp_cells = list(state.cells)
    for cell in temp_cells:
        cellularDistanceFilter(cell,deviation)
    print(temp_cells is state.cells)
    return tuple(temp_cells)

# Is not functional, since it removes from cell and cell neighbor
# If it is passed a copy, it is effectivily functional
def cellularDistanceFilter(cell,deviation):
    cell.sortNeighbors()
    # this is the furthest distance to allowed neighbor. Starts at the shortest
    maxDistance = cell.neighbors[0].distance_to_border if (len(cell.neighbors) > 0) else 0
    # Bypasses isWithinAllowedDistance() computation after it fails the first time
    pastAllowed = False
    for possibleNeighbor in list(cell.neighbors):
        # possibly faster to nest, but not as clean
        if (not pastAllowed) and (isWithinAllowedDistance(cell,possibleNeighbor,maxDistance,deviation)): 
            maxDistance = possibleNeighbor.distance_to_border
        else:
            pastAllowed = True
        if pastAllowed:
            cell.removeNeighbor(possibleNeighbor)



#TODO:: This is messy, and both booleans are probably not neccessary
# checks if neighbor is within the limit on distances past the current maxDistance
def isWithinAllowedDistance(cell, possibleNeighbor, maxDistance,deviation):
    distLimit = 1.75*(cell.radius + possibleNeighbor.cell.radius)
    neighborInDistLimit = possibleNeighbor.distance_to_border < distLimit
    neighborInDevationLimit = possibleNeighbor.distance_to_border < maxDistance+deviation
    return neighborInDistLimit and neighborInDevationLimit