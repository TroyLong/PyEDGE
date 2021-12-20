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
from analysis.tree import Rectangle as rect
from . import mergeSort as ms



def distanceFilter(cells,deviation):
    for cell in cells:
        deviation = deviation
        cell[ct.NEIGHBORGUESSES] = ms.mergeSortNeighbors(cell[ct.NEIGHBORGUESSES])
        if len(cell[ct.NEIGHBORGUESSES]) > 0:
            maxDistance = cell[ct.NEIGHBORGUESSES][0][1]
            for possibleNeighbor in cell[ct.NEIGHBORGUESSES]:
                distLimit = 1.75*(cell[ct.RADIUS] + possibleNeighbor[0][ct.RADIUS])
                if (possibleNeighbor[1] < distLimit) and (possibleNeighbor[1] < maxDistance+deviation):
                    cell[ct.NEIGHBORS].append(possibleNeighbor[0])
                else:
                    break
                maxDistance = possibleNeighbor[1]



def passThroughMultipleAreasFilter(cells,image):
    for point1 in cells:
        tempList = list()
        for point2 in point1[ct.NEIGHBORS]:
            #This should restrict the algorithm to look along the line segment, but it misses near points, whose radii are in the box
            bottomPointX = point1[ct.CENTER][0] if point1[ct.CENTER][0]<point2[ct.CENTER][0] else point2[ct.CENTER][0]
            bottomPointY = point1[ct.CENTER][1] if point1[ct.CENTER][1]<point2[ct.CENTER][1] else point2[ct.CENTER][1]
            height = np.abs(point2[ct.CENTER][1]-point1[ct.CENTER][1])
            width = np.abs(point2[ct.CENTER][0]-point1[ct.CENTER][0])
            boundingRect = rect(bottomPointX,bottomPointY,height,width)
            #This should become true if a line passes through it's neighbor
            intersects = False
            for circle in point1[ct.NEIGHBORS]:
                height = np.abs(point2[ct.CENTER][1]-point1[ct.CENTER][1])+circle[ct.RADIUS]
                width = np.abs(point2[ct.CENTER][0]-point1[ct.CENTER][0])+circle[ct.RADIUS]
                boundingRect = rect(bottomPointX,bottomPointY,height,width)
                # The circle isn't point2 and it is between point1 and point2
                #TODO:: This doesn't account for when the point goes from being to far on one side, to being to far on the other. 0|-----|0
                #TODO:: I might make two rectangles and see if the segments cross.
                if ((circle[ct.CENTER] == point2[ct.CENTER]) or not(boundingRect.isPositionInside(circle[ct.CENTER]) or
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
                distance = (np.abs(np.cross(np.asarray(point2[ct.CENTER])-np.asarray(point1[ct.CENTER]),
                                            np.asarray(point1[ct.CENTER])-np.asarray(circle[ct.CENTER])))
                                    /np.linalg.norm(np.asarray(point2[ct.CENTER])-np.asarray(point1[ct.CENTER])))
                if distance <= circle[ct.RADIUS]:
                    intersects = True
                    break
            if not intersects:
                tempList.append(point2)
        point1[ct.NEIGHBORS] = tempList



#This checks for a one to one relationship between neighboring cells
def oneToOneFilter(cells):
    for cell in cells:
        for neighbor in cell[ct.NEIGHBORS]:
            oneToOne = False
            for neighorsNeighbor in neighbor[ct.NEIGHBORS]:
                if cell[ct.CENTER] == neighorsNeighbor[ct.CENTER]:
                    oneToOne = True
            if not oneToOne:
                cell[ct.NEIGHBORS].remove(neighbor)