########################
## Imported Libraries ##
########################
from enum import Enum, auto
########################
## Internal Libraries ##
########################
from dataTypes.cell import cell


# The enum is for type completion for my cell's neighbor's dictionary's keys.
class cellNeighborTraits(Enum):
    CELL = auto()
    DISTANCE_TO_BORDER = auto()

# TODO:: should distance_to_border be distance between each exterior?
# A dictionary is used over a traditional object for speed
cellNeighbor = {cellNeighborTraits.CELL:cell.copy(), 
                cellNeighborTraits.DISTANCE_TO_BORDER:0}