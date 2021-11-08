# This holds the state information for each image loaded into the main program

from enum import Enum

# The enum is for type completion for my deque dictionary's keys.
class imageStateTraits(Enum):
    IMAGE = 0
    FILTERED_IMAGE = 1
    NEIGHBOR_IMAGE = 2
    #How far can a center be away from the last center and be in the same set
    DEVIATION = 3
    #Sets a longest possible neighbor distance. Really important variable
    MAX_NEIGHBHOR_DIST = 4
    #Allows a first order approximation to speed up tree branching. Small numbers don't look far enough, large numbers take a long time
    UPPER_CUTOFF_DIST = 5


# A dictionary is used over a traditional object for speed
imageState = {imageStateTraits.IMAGE:None,imageStateTraits.DEVIATION:15,imageStateTraits.MAX_NEIGHBHOR_DIST:80000,imageStateTraits.UPPER_CUTOFF_DIST:5000}