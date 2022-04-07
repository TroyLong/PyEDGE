from enum import Enum, auto

# The enum is for type completion for my dictionary's keys.



class imageStateTraits(Enum):
    # Locks commands that rely on an image to work until an image is loaded. Being a boolean should make it faster
    IMAGE_OPENED = auto()
    # Images
    IMAGE = auto()
    FILTERED_IMAGE = auto()
    NEIGHBOR_IMAGE = auto()

    #Cells
    CELLS = auto()
    CELL_INDEX = auto()
    #Cells Statistics
    MEAN_CELL_RADII = auto()

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



