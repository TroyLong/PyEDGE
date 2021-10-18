#TODO:: Neighborguesses is just taking up extra memory.
#TODO:: Neighbors might need to be its own datatype.

from enum import Enum

# The enum is for type completion for my cell dictionary's keys.
class cellTraits(Enum):
    CENTER = 0
    VERTICIES = 1
    AREA = 2
    RADIUS = 3
    NEIGHBORGUESSES = 4
    NEIGHBORS = 5

# A dictionary is used over a traditional object for speed
cell = {cellTraits.CENTER:(0,0), cellTraits.VERTICIES:list(), cellTraits.AREA:0, cellTraits.RADIUS:0, cellTraits.NEIGHBORGUESSES:list(), cellTraits.NEIGHBORS:list()}