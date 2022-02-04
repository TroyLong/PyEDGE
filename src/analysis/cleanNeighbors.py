########################
##        About       ##
########################
# This should ensure that all neighbors are mutually connected.
# There is probably a better way to do this, but I need it done
# in the first place before I start optimizing everything.
# This knowingly breaks functional form to change the neighbor's neighbor list
########################
## Internal Libraries ##
########################
import dataTypes.cell as ce
from dataTypes.cell import cellTraits as ct
from dataTypes.cellNeighbor import cellNeighborTraits as cnt
import dataTypes.imageState as iS
from dataTypes.imageStateTraits import imageStateTraits as iST
from analysis.filters.neighborFilters.tooFewNeighborsFilter import tooFewNeighborsFilter
from analysis.filters.neighborFilters.distanceFilter import distanceFilter
from analysis.filters.neighborFilters.passThroughMultipleAreasFilter import passThroughMultipleAreasFilter
from . import walkTree as walkTree
from . import tree as tree

def cleanNeighbors(state):
    cells = state[iST.CELLS]
    for cell in cells:
        for neighbor in cell[ct.NEIGHBORS]:
            neighbor = neighbor[cnt.CELL]
            cleanNeighbor(cell, neighbor)


# This knowingly breaks functional form
def cleanNeighbor(cell, neighbor):
    if not doesNeighborContainCell(cell, neighbor):
        neighbor[ct.NEIGHBORS] = tuple(list(neighbor[ct.NEIGHBORS]).append(cell))
        print("Recovered")


# Compares a cell and its neighbor. Checks if the cell is in its neighbor's neighbor list
def doesNeighborContainCell(cell, neighbor):
    for possibleMutualCell in neighbor:
        if ce.cellEqual(cell, possibleMutualCell):
            return True
    return False