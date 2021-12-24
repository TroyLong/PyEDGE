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
    NEIGHBORS = auto()

# A dictionary is used over a traditional object for speed
# TODO:: I'm not sure if I should use a tuple or a list for neighbors seeing as how often it will be changed
# TODO:: I need to change verticies to tuple
cell = {cellTraits.CENTER:(0,0), cellTraits.VERTICIES:list(), cellTraits.AREA:0, cellTraits.RADIUS:0, cellTraits.NEIGHBORS:tuple()}