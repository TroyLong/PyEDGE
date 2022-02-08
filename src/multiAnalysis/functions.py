from dataTypes.cell import cell
from dataTypes.cell import cellDist
import dataTypes.cell as ce
from dataTypes.cellNeighbor import cellNeighbor
from dataTypes.dataTypeTraits import cellTraits as ct
from dataTypes.dataTypeTraits import cellNeighborTraits as cnt
from dataTypes.dataTypeTraits import imageStateTraits as ist
from dataTypes.imageState import imageState

from numpy import sqrt

# use two overlapping trees, and compare from each other? Not sure it is worth the computational time
# This would be a great place for dynamic programming, saving the distances between each node?
# I'm going to brute force it for now


def doodle(state1, state2):
    pass

# TODO:: This a jank way to do this
# This could possibly benifit from being placed in a tree
def findCellOverlap(cells1, cells2):
    tempCells = list()
    for cell1 in cells1:
        for cell2 in cells2:
            if cellsOverlap(cell1,cell2):
                tempCells.append(ce.createAverageCell(cell1,cell2))
                break
    return tuple(tempCells)

# Returns true if two cells geometries overlap
def cellsOverlap(cell1, cell2):
    return cellDist(cell1,cell2) < (cell1[ct.RADIUS]+cell2[ct.RADIUS])
