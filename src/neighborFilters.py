import cv2 as cv
import numpy as np
import mergeSort as ms
from cell import cellTraits as ct
from math import dist


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



#TODO:: Why does this allow certain lines to pass through the areas. Term3 has a lot of power here
def passThroughMultipleAreasFilter(cells,image):
    color1 = 255
    color2 = 0
    for point1 in cells:
        for point2 in point1[ct.NEIGHBORS]:
            intersects = False
            for circle in point1[ct.NEIGHBORS]:
                if circle[ct.CENTER] == point2[ct.CENTER]:
                    continue
                distance = (np.abs(np.cross(np.asarray(point2[ct.CENTER])-np.asarray(point1[ct.CENTER]),
                                            np.asarray(point1[ct.CENTER])-np.asarray(circle[ct.CENTER])))
                                    /np.linalg.norm(np.asarray(point2[ct.CENTER])-np.asarray(point1[ct.CENTER])))
                cv.circle(image, (circle[ct.CENTER][0],circle[ct.CENTER][1]), int(circle[ct.RADIUS]), (color1, color2, 0), 3)
                cv.line(image,point1[ct.CENTER],point2[ct.CENTER],(color1,color2,0), 2)
                if distance < circle[ct.RADIUS]:
                    intersects = True
                    #cv.line(image,point1[ct.CENTER],point2[ct.CENTER],(color1,color2,0), 2)
                    #cv.circle(image, (circle[ct.CENTER][0],circle[ct.CENTER][1]), int(distance), (color1, color2,0), -1)
                    break
        color1-=1
        color2+=1
            #if intersects:
            #    pass
                #point1[ct.NEIGHBORS].remove(point2)



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