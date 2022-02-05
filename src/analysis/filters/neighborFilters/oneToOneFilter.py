from copy import deepcopy
import dataTypes.cell as ce
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT
from dataTypes.dataTypeTraits import imageStateTraits as iST

def oneToOneFilter(state):
    tempCells = deepcopy(state[iST.CELLS])
    for cell in tempCells:
        for neighbor in cell:
            if cell not in neighbor[cNT.CELL][cT.NEIGHBORS]:
                ce.removeNeighborOneWay(cell,neighbor)
