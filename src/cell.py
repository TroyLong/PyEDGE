from enum import Enum

# The enum is for type completion for my cell dictionary's keys.
class cellTraits(Enum):
    CENTER = 0
    VERTICIES = 1
    AREA = 2
    NEIGHBORGUESSES = 3
    NEIGHBORS = 4

# A dictionary is used over a traditional object for speed
cell = {cellTraits.CENTER:(0,0), cellTraits.VERTICIES:list(), cellTraits.AREA:0, cellTraits.NEIGHBORGUESSES:list(), cellTraits.NEIGHBORS:list()}