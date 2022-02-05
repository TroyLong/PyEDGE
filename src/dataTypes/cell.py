########################
## Imported Libraries ##
########################
from enum import Enum, auto
from math import dist
from types import CellType
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT



# A dictionary is used over a traditional object for speed
# TODO:: I'm not sure if I should use a tuple or a list for
# neighbors seeing as how often it will be changed
cell = {cT.CENTER:(0,0), cT.VERTICIES:tuple(),
        cT.AREA:0, cT.RADIUS:0, cT.NEIGHBORS:tuple()}

def cellDist(cell1, cell2):
    return dist(cell1[cT.CENTER],cell2[cT.CENTER])

def cellEqual(cell1, cell2):
    return cell1[cT.CENTER] == cell2[cT.CENTER]
    


def isCellNeighbor(cellNeighbors,possibleNeighbor):
    return possibleNeighbor in cellNeighbors



# TODO:: Not sure if this is going to be useful
# Returns two new tuples with connection between cell1 and cell2 broken
def removeNeighborTwoWay(cell, neighbor):
    cell1Neighbors = removeNeighborOneWay(cell,neighbor)
    cell2Neighbors = removeNeighborOneWay(neighbor[cNT.CELL],cell)
    return cell1Neighbors,cell2Neighbors

def removeNeighborOneWay(cell, neighbor):
    cellNeighbors = list(cell[cT.NEIGHBORS])
    try:
        cellNeighbors.remove(neighbor)
    except ValueError:
        pass
    return tuple(cellNeighbors)



# Adapter to the sorted function
def sortNeighbors(cell):
    return sorted(cell[cT.NEIGHBORS], key=lambda cellN: cellN[cNT.DISTANCE_TO_BORDER])  

 