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
from dataTypes.cell import cellTraits as ct
from dataTypes.cellNeighbor import cellNeighborTraits as cnt
from analysis.tree import Rectangle as rect
from . import mergeSort as ms



# Takes neighbors out of the neighbor list if they are 
def distanceFilter(cells,deviation):
    for cell in cells:
        # temporary list for appending new results to. Will be converted to tuple
        finalNeighbors = list()
        # takes current list of neighbors around the cell, and sorts them by distance to the neighbor's border
        cell[ct.NEIGHBORS] = ms.mergeSortNeighbors(cell[ct.NEIGHBORS])
        if len(cell[ct.NEIGHBORS]) > 0:
            # this is the furthest distance to allowed neighbor. Starts at the shortest
            maxDistance = cell[ct.NEIGHBORS][0][cnt.DISTANCE_TO_BORDER]
            for possibleNeighbor in cell[ct.NEIGHBORS]:
                # checks if neighbor is within the limit on distances past the current maxDistance
                distLimit = 1.75*(cell[ct.RADIUS] + possibleNeighbor[cnt.CELL][ct.RADIUS])
                if (possibleNeighbor[cnt.DISTANCE_TO_BORDER] < distLimit) and (possibleNeighbor[cnt.DISTANCE_TO_BORDER] < maxDistance+deviation):
                    # if neighbor is in limit, adds it to final neighbor list
                    finalNeighbors.append(possibleNeighbor)
                else:
                    # otherwise stop checking as the list is sorted, and no others will be successful
                    break
                # set new max distance
                maxDistance = possibleNeighbor[cnt.DISTANCE_TO_BORDER]
        # sets the neighbor list to be the new one based on the filter    
        cell[ct.NEIGHBORS] = tuple(finalNeighbors)



# Takes neighbors out of the neighbor list if they pass through more than one cell
def passThroughMultipleAreasFilter(cells,image):
    for cell in cells:
        # This is the center of the cell. Simplifies math
        point1 = cell[ct.CENTER]
        # temporary list for appending new results to. Will be converted to tuple
        finalNeighbors = list()
        for neighbor in cell[ct.NEIGHBORS]:
            # This is the center of the neighbor cell. Simplifies math
            point2 = neighbor[cnt.CELL][ct.CENTER]
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
            for otherNeighbor in cell[ct.NEIGHBORS]:
                circle = otherNeighbor[cnt.CELL]
                height = np.abs(point2[1]-point1[1])+circle[ct.RADIUS]
                width = np.abs(point2[0]-point1[0])+circle[ct.RADIUS]
                boundingRect = rect(bottomPointX,bottomPointY,height,width)
                # The circle isn't point2 and it is between point1 and point2
                #TODO:: This doesn't account for when the point goes from being to far on one side, to being to far on the other. 0|-----|0
                #TODO:: I might make two rectangles and see if the segments cross.
                if ((circle[ct.CENTER] == point2) or not(boundingRect.isPositionInside(circle[ct.CENTER]) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0]+circle[ct.RADIUS],circle[ct.CENTER][1])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0]-circle[ct.RADIUS],circle[ct.CENTER][1])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0],circle[ct.CENTER][1]+circle[ct.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0],circle[ct.CENTER][1]-circle[ct.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0]+circle[ct.RADIUS],circle[ct.CENTER][1]+circle[ct.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0]-circle[ct.RADIUS],circle[ct.CENTER][1]-circle[ct.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0]+circle[ct.RADIUS],circle[ct.CENTER][1]-circle[ct.RADIUS])) or
                                                                    boundingRect.isPositionInside((circle[ct.CENTER][0]-circle[ct.RADIUS],circle[ct.CENTER][1]+circle[ct.RADIUS]))
                                                                    )):
                    continue
                #Finds the perpendicular distance between the line of point1-2 and the circle's center
                distance = (np.abs(np.cross(np.asarray(point2)-np.asarray(point1),
                                            np.asarray(point1)-np.asarray(circle[ct.CENTER])))
                                    /np.linalg.norm(np.asarray(point2)-np.asarray(point1)))
                if distance <= circle[ct.RADIUS]:
                    intersects = True
                    break
            if not intersects:
                finalNeighbors.append(neighbor)
        cell[ct.NEIGHBORS] = tuple(finalNeighbors)



#This checks for a one to one relationship between neighboring cells
#def oneToOneFilter(cells):
#    for cell in cells:
#        for neighbor in cell[ct.NEIGHBORS]:
#            oneToOne = False
#            for neighorsNeighbor in neighbor[ct.NEIGHBORS]:
#                if cell[ct.CENTER] == neighorsNeighbor[ct.CENTER]:
#                    oneToOne = True
#            if not oneToOne:
#                cell[ct.NEIGHBORS].remove(neighbor)