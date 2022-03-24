########################
##        About       ##
########################
# This removes cells that don't have enough neighbors
########################
## Imported Libraries ##
########################
from copy import deepcopy
import dataTypes.cell as ce
from dataTypes.dataTypeTraits import cellTraits as cT


# Functional Form
def tooFewNeighborsFilter(state,cutoff):
    tempCells = list(deepcopy(state.cells))
    for cell in tempCells:
        if len(cell[cT.NEIGHBORS]) <= cutoff:
            for neighbor in cell[cT.NEIGHBORS]:
                ce.removeNeighborTwoWay(cell,neighbor)
            tempCells.remove(cell)
    return tuple(tempCells)