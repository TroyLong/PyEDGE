########################
## Imported Libraries ##
########################
from enum import Enum, auto
from math import dist
from types import CellType


# The enum is for type completion for my cell dictionary's keys.
class cellTraits(Enum):
    CENTER = auto()
    VERTICIES = auto()
    AREA = auto()
    RADIUS = auto()
    NEIGHBORS = auto()

# A dictionary is used over a traditional object for speed
# TODO:: I'm not sure if I should use a tuple or a list for
# neighbors seeing as how often it will be changed
cell = {cellTraits.CENTER:(0,0), cellTraits.VERTICIES:tuple(),
        cellTraits.AREA:0, cellTraits.RADIUS:0, cellTraits.NEIGHBORS:tuple()}

def cellDist(cell1, cell2):
    return dist(cell1[cellTraits.CENTER],cell2[cellTraits.CENTER])

def cellEqual(cell1, cell2):
    return cell1[cellTraits.CENTER] == cell2[cellTraits.CENTER]
    


# Returns two new tuples with connection between cell1 and cell2 broken
def removeNeighborTwoWay(cell1, cell2):
    cell1Neighbors = removeNeighborOneWay(cell1,cell2)
    cell2Neighbors = removeNeighborOneWay(cell2,cell1)
    return cell1Neighbors,cell2Neighbors

# Returns new tuple of cell1's neighbors without cell2.
def removeNeighborOneWay(cell1, cell2):
    cellNeighbors = list(cell1[cellTraits.NEIGHBORS].copy())
    cellNeighbors.remove(cell2)
    return tuple(cellNeighbors)