########################
##        About       ##
########################
# This removes cells that don't have enough neighbors
########################
## Imported Libraries ##
########################
from copy import deepcopy
import dataTypes.cell as ce


# Functional Form
def tooFewNeighborsFilter(state,cutoff):
    tempCells = list(deepcopy(state.cells))
    for cell in tempCells:
        if len(cell.neighbors) <= cutoff:
            for neighbor in cell.neighbors:
                ce.removeNeighborTwoWay(cell,neighbor)
            tempCells.remove(cell)
    return tuple(tempCells)