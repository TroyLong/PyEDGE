#TODO:: Neighborguesses is just taking up extra memory.
#TODO:: Neighbors might need to be its own datatype.

########################
## Imported Libraries ##
########################
from enum import Enum, auto

# The enum is for type completion for my cell dictionary's keys.
class cellTraits(Enum):
    CENTER = auto()
    VERTICIES = auto()
    AREA = auto()
    RADIUS = auto()
    NEIGHBORGUESSES = auto()
    NEIGHBORS = auto()

# A dictionary is used over a traditional object for speed
cell = {cellTraits.CENTER:(0,0), cellTraits.VERTICIES:list(), cellTraits.AREA:0, cellTraits.RADIUS:0, cellTraits.NEIGHBORGUESSES:list(), cellTraits.NEIGHBORS:list()}
