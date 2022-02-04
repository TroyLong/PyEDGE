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
    


# Returns two new tuples with connection between cell1 and cell2 broken
def removeNeighborTwoWay(cell1, cell2):
    cell1Neighbors = removeNeighborOneWay(cell1,cell2)
    cell2Neighbors = removeNeighborOneWay(cell2,cell1)
    return cell1Neighbors,cell2Neighbors

# Returns new tuple of cell1's neighbors without cell2.
def removeNeighborOneWay(cell1, cell2):
    cellNeighbors = list(cell1[cT.NEIGHBORS].copy())
    cellNeighbors.remove(cell2)
    return tuple(cellNeighbors)

def sortNeighbors(cell):
    return sorted(cell[cT.NEIGHBORS], key=lambda cellN: cellN[cNT.DISTANCE_TO_BORDER])  