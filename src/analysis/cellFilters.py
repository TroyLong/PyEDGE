########################
## Internal Libraries ##
########################
import dataTypes.imageState as iS
from dataTypes.imageStateTraits import imageStateTraits as iST
from dataTypes.cell import cellTraits as cT


# Removes cells to small to be real cells. Recreates cells to be tuple ready
# Currently doesn't protect against negative numbers
def removeOutlierSmallRadii(state,deviations):
    cells = state[iST.CELLS]
    meanRadius = iS.meanCellRadii(state)
    deviation = iS.cellRadiusDeviation(state)
    tempCells = list()
    for cell in cells:
        if cell[cT.RADIUS] > (meanRadius - (deviations * deviation)):
            tempCells.append(cell)
    return tempCells