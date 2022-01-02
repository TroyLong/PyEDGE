########################
##        About       ##
########################
# This removes neighbors that are aligned with other neighbors
########################
## Imported Libraries ##
########################
import numpy as np
########################
## Imported Libraries ##
########################
from dataTypes.cell import cellTraits as cT
from dataTypes.cellNeighbor import cellNeighborTraits as cnt
from dataTypes.imageStateTraits import imageStateTraits as iST
from analysis.tree import Rectangle as rect


# TODO:: Break this up further
# Functional Form
# Takes neighbors out of the neighbor list if they pass through more than one cell
def passThroughMultipleAreasFilter(state):
    # cells returned
    tempCells = list()
    # do this for every cell in the state
    for cell in state[iST.CELLS]:
        cell = cell.copy()
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
                if isRectangleNotBounding(circle,point2,boundingRect):
                    continue
                distance = findPerpendicularDist(circle,point1,point2)
                if distance <= circle[cT.RADIUS]:
                    intersects = True
                    break
            if not intersects:
                finalNeighbors.append(neighbor)
        cell[cT.NEIGHBORS] = tuple(finalNeighbors)
        tempCells.append(cell)
    return tuple(tempCells)


# The circle isn't point2 and it is between point1 and point2
#TODO:: This doesn't account for when the point goes from being to far on one side, to being to far on the other. 0|-----|0
#TODO:: I might make two rectangles and see if the segments cross.
def isRectangleNotBounding(circle,point2,boundingRect):
    return ((circle[cT.CENTER] == point2) or not(boundingRect.isPositionInside(circle[cT.CENTER]) or
            boundingRect.isPositionInside((circle[cT.CENTER][0]+circle[cT.RADIUS],circle[cT.CENTER][1])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0]-circle[cT.RADIUS],circle[cT.CENTER][1])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0],circle[cT.CENTER][1]+circle[cT.RADIUS])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0],circle[cT.CENTER][1]-circle[cT.RADIUS])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0]+circle[cT.RADIUS],circle[cT.CENTER][1]+circle[cT.RADIUS])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0]-circle[cT.RADIUS],circle[cT.CENTER][1]-circle[cT.RADIUS])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0]+circle[cT.RADIUS],circle[cT.CENTER][1]-circle[cT.RADIUS])) or
            boundingRect.isPositionInside((circle[cT.CENTER][0]-circle[cT.RADIUS],circle[cT.CENTER][1]+circle[cT.RADIUS]))
            ))


#Finds the perpendicular distance between the line of point1-2 and the circle's center
def findPerpendicularDist(circle,point1,point2):
    return (np.abs(np.cross(np.asarray(point2)-np.asarray(point1),
            np.asarray(point1)-np.asarray(circle[cT.CENTER])))
            /np.linalg.norm(np.asarray(point2)-np.asarray(point1)))