########################
##        About       ##
########################
# These are a series of tests for neighbor finding.
# Split from neighborAnalysis.py because they are dealing with the data in completely different ways
########################
## Imported Libraries ##
########################
import cv2 as cv
import numpy as np
from math import dist
from types import CellType
########################
## Imported Libraries ##
########################
from dataTypes.cell import cellTraits as cT
from dataTypes.cellNeighbor import cellNeighborTraits as cnt
from analysis.tree import Rectangle as rect
from . import mergeSort as ms



def tooFewNeighborsFilter(cells,cutoff):
    tempCells = list()
    for cell in cells:
        if cell[cT.NEIGHBORS] > cutoff:
            tempCells.append(cell)
    return tuple(tempCells())




# Takes neighbors out of the neighbor list if they are 
def distanceFilter(cells,deviation):
    tempCells = list()
    for cell in cells:
        tempCells.append(cellularDistanceFilter(cell,deviation))
    return tuple(tempCells)

#TODO:: To make this better, I should first sort the neighbors somewhere else, perhaps under a clean data function
def cellularDistanceFilter(cell,deviation):
    # sorts neighbors by distance
    sortedNeighbors = ms.mergeSortNeighbors(cell[cT.NEIGHBORS])
    realNeighbors = list()
    # returned cell datastructure. Does not alter the original cell
    tempCell = cell.copy()
    maxDistance = 0
    if len(cell[cT.NEIGHBORS]) > 0:
        # this is the furthest distance to allowed neighbor. Starts at the shortest
        maxDistance = cell[cT.NEIGHBORS][0][cnt.DISTANCE_TO_BORDER]
    for possibleNeighbor in sortedNeighbors:
        if isWithinAllowedDistance(cell,possibleNeighbor,maxDistance,deviation):
            # if neighbor is in limit, adds it to final neighbor list
            realNeighbors.append(possibleNeighbor)
        else:
            # the list is sorted, and no others will be successful
            break
        # set new max distance
        maxDistance = possibleNeighbor[cnt.DISTANCE_TO_BORDER]
    tempCell[cT.NEIGHBORS] = realNeighbors
    # sets the neighbor list to be the new one based on the filter    
    return tempCell




#TODO:: This is messy, and both booleans are probably not neccessary
# checks if neighbor is within the limit on distances past the current maxDistance
def isWithinAllowedDistance(cell, possibleNeighbor, maxDistance,deviation):
    distLimit = 1.75*(cell[cT.RADIUS] + possibleNeighbor[cnt.CELL][cT.RADIUS])
    neighborInDistLimit = possibleNeighbor[cnt.DISTANCE_TO_BORDER] < distLimit
    neighborInDevationLimit = possibleNeighbor[cnt.DISTANCE_TO_BORDER] < maxDistance+deviation
    return neighborInDistLimit and neighborInDevationLimit


# Takes neighbors out of the neighbor list if they pass through more than one cell
def passThroughMultipleAreasFilter(cells,image):
    for cell in cells:
        # This is the center of the cell. Simplifies math
        point1 = cell[cT.CENTER]
        # temporary list for appending new results to. Will be converted to tuple
        finalNeighbors = list()
        for neighbor in cell[cT.NEIGHBORS]:
            # This is the center of the neighbor cell. Simplifies math
            point2 = neighbor[cnt.CELL][cT.CENTER]
            #TODO:: This should restrict the algorithm to look along the line segment, but it misses near points, whose radii are in the box
            bottomPointX = point1[0] if point1[0]<point2[0] else point2[0]
            bottomPointY = point1[1] if point1[1]<point2[1] else point2[1]
            height = np.abs(point2[1]-point1[1])
            width = np.abs(point2[0]-point1[0])
            boundingRect = rect(bottomPointX,bottomPointY,height,width)
            #This should become true if a line passes through it's neighbor
            intersects = False
            # This checks the neighbor list to see if there is a line through the cell, the current neighbor, and any other neighbors
            # TODO:: There should be a clever way to get the big O to behave better, but that is for another day
            for otherNeighbor in cell[cT.NEIGHBORS]:
                circle = otherNeighbor[cnt.CELL]
                height = np.abs(point2[1]-point1[1])+circle[cT.RADIUS]
                width = np.abs(point2[0]-point1[0])+circle[cT.RADIUS]
                boundingRect = rect(bottomPointX,bottomPointY,height,width)
                # The circle isn't point2 and it is between point1 and point2
                #TODO:: This doesn't account for when the point goes from being to far on one side, to being to far on the other. 0|-----|0
                #TODO:: I might make two rectangles and see if the segments cross.
                if ((circle[cT.CENTER] == point2) or not(boundingRect.isPositionInside(circle[cT.CENTER]) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0]+circle[cT.RADIUS],circle[cT.CENTER][1])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0]-circle[cT.RADIUS],circle[cT.CENTER][1])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0],circle[cT.CENTER][1]+circle[cT.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0],circle[cT.CENTER][1]-circle[cT.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0]+circle[cT.RADIUS],circle[cT.CENTER][1]+circle[cT.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0]-circle[cT.RADIUS],circle[cT.CENTER][1]-circle[cT.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0]+circle[cT.RADIUS],circle[cT.CENTER][1]-circle[cT.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[cT.CENTER][0]-circle[cT.RADIUS],circle[cT.CENTER][1]+circle[cT.RADIUS]))
                                                                    )):
                    continue
                #Finds the perpendicular distance between the line of point1-2 and the circle's center
                distance = (np.abs(np.cross(np.asarray(point2)-np.asarray(point1),
                                            np.asarray(point1)-np.asarray(circle[cT.CENTER])))
                                    /np.linalg.norm(np.asarray(point2)-np.asarray(point1)))
                if distance <= circle[cT.RADIUS]:
                    intersects = True
                    break
            if not intersects:
                finalNeighbors.append(neighbor)
        cell[cT.NEIGHBORS] = tuple(finalNeighbors)



#This checks for a one to one relationship between neighboring cells
#def oneToOneFilter(cells):
#    for cell in cells:
#        for neighbor in cell[cT.NEIGHBORS]:
#            oneToOne = False
#            for neighorsNeighbor in neighbor[cT.NEIGHBORS]:
#                if cell[cT.CENTER] == neighorsNeighbor[cT.CENTER]:
#                    oneToOne = True
#            if not oneToOne:
#                cell[cT.NEIGHBORS].remove(neighbor)