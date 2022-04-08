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
def too_few_neighbors_filter(state,cutoff):
    temp_cells = list(state.cells)
    for cell in temp_cells:
        if len(cell.neighbors) <= cutoff:
            for neighbor in cell.neighbors:
                cell.remove_neighbor(neighbor)
            temp_cells.remove(cell)
    return tuple(temp_cells)