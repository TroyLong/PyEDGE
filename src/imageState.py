# This holds the state information for each image loaded into the main program

from enum import Enum, auto
import numpy as np

# The enum is for type completion for my deque dictionary's keys.
class imageStateTraits(Enum):
    #Images
    IMAGE = auto()
    FILTERED_IMAGE = auto()
    NEIGHBOR_IMAGE = auto()

    #Cells
    CELLS = auto()

    #Image processing options
    FILTER_DIAMETER = auto()
    SIGMA_COLOR = auto()
    SIGMA_SPACE = auto()
    ADAPTIVE_BLOCKSIZE = auto()

    #Image Analysis
    #How far can a center be away from the last center and be in the same set
    DEVIATION = auto()
    #Sets a longest possible neighbor distance. Really important variable
    MAX_NEIGHBHOR_DIST = auto()
    #Allows a first order approximation to speed up tree branching. Small numbers don't look far enough, large numbers take a long time
    UPPER_CUTOFF_DIST = auto()

emptyImage = np.zeros(np.shape([1,1,3]),dtype=np.uint8)

# A dictionary is used over a traditional object for speed
imageState = {imageStateTraits.IMAGE:emptyImage.copy(),imageStateTraits.FILTERED_IMAGE:emptyImage.copy(),
                imageStateTraits.NEIGHBOR_IMAGE:emptyImage.copy(),
                imageStateTraits.CELLS:[],
                imageStateTraits.FILTER_DIAMETER:0,imageStateTraits.SIGMA_COLOR:0,
                imageStateTraits.SIGMA_SPACE:0,imageStateTraits.ADAPTIVE_BLOCKSIZE:0,
                imageStateTraits.DEVIATION:15,imageStateTraits.MAX_NEIGHBHOR_DIST:80000,
                imageStateTraits.UPPER_CUTOFF_DIST:5000}