########################
##        About       ##
########################
# This should ensure that all neighbors are mutually connected.
# There is probably a better way to do this, but I need it done
# in the first place before I start optimizing everything.
# This knowingly breaks functional form to change the neighbor's neighbor list
########################
## External Libraries ##
########################
import logging
########################
## Internal Libraries ##
########################
import dataTypes.cell as ce
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT
import dataTypes.imageState as iS
from analysis.filters.neighborFilters.tooFewNeighborsFilter import tooFewNeighborsFilter
from analysis.filters.neighborFilters.distanceFilter import distanceFilter
from analysis.filters.neighborFilters.passThroughMultipleAreasFilter import passThroughMultipleAreasFilter
from . import walkTree as walkTree
from . import tree as tree

def cleanNeighbors(state):
    cells = state.cells
    for cell in cells:
        for neighbor in cell[cT.NEIGHBORS]:
            neighbor = neighbor[cNT.CELL]
            cleanNeighbor(cell, neighbor)


# This knowingly breaks functional form
def cleanNeighbor(cell, neighbor):
    if not doesNeighborContainCell(cell, neighbor):
        neighbor[cT.NEIGHBORS] = tuple(list(neighbor[cT.NEIGHBORS]).append(cell))


# Compares a cell and its neighbor. Checks if the cell is in its neighbor's neighbor list
def doesNeighborContainCell(cell, neighbor):
    for possibleMutualCell in neighbor:
        if ce.cellEqual(cell, possibleMutualCell):
            return True
    return False