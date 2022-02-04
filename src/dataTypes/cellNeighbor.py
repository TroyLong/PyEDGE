########################
## Imported Libraries ##
########################
from enum import Enum, auto
########################
## Internal Libraries ##
########################
from dataTypes.cell import cell
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT



# A dictionary is used over a traditional object for speed
cellNeighbor = {cNT.CELL:cell, 
                cNT.DISTANCE_TO_BORDER:0}