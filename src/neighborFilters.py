import cv2 as cv
import numpy as np
import mergeSort as ms
from cell import cellTraits as ct
from math import dist


def findNeighbors(cells,deviation):
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



#TODO:: Why does this allow certain lines to pass through the areas. Term3 has a lot of power here
def passThroughMultipleAreasFilter(cells,image):
    for point1 in cells:
        for point2 in point1[ct.NEIGHBORS]:
            term3 = dist(point1[ct.CENTER],point2[ct.CENTER])
            intersects = False
            for circle in point1[ct.NEIGHBORS]:
                if circle == point2:
                    continue
                term1 = (point2[ct.CENTER][0]-point1[ct.CENTER][0])*(point1[ct.CENTER][1]-circle[ct.CENTER][1])
                term2 = (point1[ct.CENTER][0]-circle[ct.CENTER][0])*(point2[ct.CENTER][1]-point1[ct.CENTER][1])
                distance = np.abs(term1-term2)/term3
                if (circle[ct.RADIUS] >=  distance):
                    print(circle[ct.RADIUS]-distance)
                    intersects = True
                    cv.line(image,point1[ct.CENTER],point2[ct.CENTER],(0,255,255), 6)
                    break
            if intersects == True:
                point1[ct.NEIGHBORS].remove(point2)



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