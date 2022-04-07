import dataTypes.cell as ce

from dataTypes.dataTypeTraits import imageStateTraits as ist

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
                tempCells.append(cell2)
                break
    return tuple(tempCells)

# TODO:: Move to cell.py
# Returns true if two cells geometries overlap
def cellsOverlap(cell1, cell2):
    return cell1.dist(cell2) <= ((cell1.radius+cell2.radius)*.75)
