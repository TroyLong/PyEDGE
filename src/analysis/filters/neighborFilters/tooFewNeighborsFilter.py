########################
##        About       ##
########################
# This removes cells that don't have enough neighbors
########################
## Imported Libraries ##
########################
from dataTypes.cell import cellTraits as cT
from dataTypes.imageStateTraits import imageStateTraits as iST


# Functional Form
def tooFewNeighborsFilter(state,cutoff):
    tempCells = list()
    for cell in state[iST.CELLS]:
        if len(cell[cT.NEIGHBORS]) > cutoff:
            tempCells.append(cell)
    return tuple(tempCells)