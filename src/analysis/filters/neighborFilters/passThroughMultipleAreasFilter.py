########################
##        About       ##
########################
# This removes neighbors that are aligned with other neighbors
########################
## Imported Libraries ##
########################
import numpy as np
import copy
########################
## Imported Libraries ##
########################
from analysis.tree import Rectangle as rect


# TODO:: Break this up further
# Functional Form
# Takes neighbors out of the neighbor list if they pass through more than one cell
def passThroughMultipleAreasFilter(state):
    # cells returned
    tempCells = list()
    # do this for every cell in the state
    for cell in state.cells:
        cell = copy.copy(cell)
        # This is the center of the cell. Simplifies math
        point1 = cell.center
        # temporary list for appending new results to. Will be converted to tuple
        finalNeighbors = list()
        for neighbor in cell.neighbors:
            # This is the center of the neighbor cell. Simplifies math
            point2 = neighbor.cell.center
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
            for otherNeighbor in cell.neighbors:
                circle = otherNeighbor.cell
                height = np.abs(point2[1]-point1[1])+circle.radius
                width = np.abs(point2[0]-point1[0])+circle.radius            
                boundingRect = rect(bottomPointX,bottomPointY,height,width)
                if isRectangleNotBounding(circle,point2,boundingRect):
                    continue
                distance = findPerpendicularDist(circle,point1,point2)
                if distance <= circle.radius:
                    intersects = True
                    break
            if not intersects:
                finalNeighbors.append(neighbor)
        cell.neighbors = tuple(finalNeighbors)
        tempCells.append(cell)
    return tuple(tempCells)


# The circle isn't point2 and it is between point1 and point2
#TODO:: This doesn't account for when the point goes from being to far on one side, to being to far on the other. 0|-----|0
#TODO:: I might make two rectangles and see if the segments cross.
def isRectangleNotBounding(circle,point2,boundingRect):
    return ((circle.center == point2) or not(boundingRect.isPositionInside(circle.center) or
            boundingRect.isPositionInside((circle.center[0]+circle.radius,circle.center[1])) or
            boundingRect.isPositionInside((circle.center[0]-circle.radius,circle.center[1])) or
            boundingRect.isPositionInside((circle.center[0],circle.center[1]+circle.radius)) or
            boundingRect.isPositionInside((circle.center[0],circle.center[1]-circle.radius)) or
            boundingRect.isPositionInside((circle.center[0]+circle.radius,circle.center[1]+circle.radius)) or
            boundingRect.isPositionInside((circle.center[0]-circle.radius,circle.center[1]-circle.radius)) or
            boundingRect.isPositionInside((circle.center[0]+circle.radius,circle.center[1]-circle.radius)) or
            boundingRect.isPositionInside((circle.center[0]-circle.radius,circle.center[1]+circle.radius))
            ))


#Finds the perpendicular distance between the line of point1-2 and the circle's center
def findPerpendicularDist(circle,point1,point2):
    return (np.abs(np.cross(np.asarray(point2)-np.asarray(point1),
            np.asarray(point1)-np.asarray(circle.center)))
            /np.linalg.norm(np.asarray(point2)-np.asarray(point1)))