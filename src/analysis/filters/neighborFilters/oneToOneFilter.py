from copy import deepcopy
import dataTypes.cell as ce

def oneToOneFilter(state):
    tempCells = deepcopy(state.cells)
    for cell in tempCells:
        for neighbor in cell:
            if cell not in neighbor.cell.neighbors:
                ce.removeNeighborOneWay(cell,neighbor)
