# TODO:: THIS MIGHT NEED TO BELONG TO THE STATE OBJECT?


# Functional Form
# Removes cells to small to be real cells. Recreates cells to be tuple ready
# Currently doesn't protect against negative numbers
def removeOutlierSmallRadii(state,deviations):
    cells = state.cells
    meanRadius = state.meanCellRadii()
    deviation = state.cellRadiusDeviation()
    tempCells = list()
    for cell in cells:
        if cell.radius > (meanRadius - (deviations * deviation)):
            tempCells.append(cell)
    return tuple(tempCells)