# This holds the state information for each image loaded into the main program

from enum import Enum, auto
import numpy as np
import tkinter as tk

# The enum is for type completion for my deque dictionary's keys.
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
imageState = {imageStateTraits.IMAGE_OPENED:False,
                imageStateTraits.IMAGE:emptyImage.copy(),imageStateTraits.FILTERED_IMAGE:emptyImage.copy(),
                imageStateTraits.NEIGHBOR_IMAGE:emptyImage.copy(),
                imageStateTraits.CELLS:[],imageStateTraits.CELL_INDEX:0,
                imageStateTraits.FILTER_DIAMETER:0,imageStateTraits.SIGMA_COLOR:0,
                imageStateTraits.SIGMA_SPACE:0,imageStateTraits.ADAPTIVE_BLOCKSIZE:0,
                imageStateTraits.DEVIATION:15,imageStateTraits.MAX_NEIGHBHOR_DIST:80000,
                imageStateTraits.UPPER_CUTOFF_DIST:5000}



# This is used by all panels and such that are handed the state
class StateMachinePanel(tk.Frame):
    def __init__(self, master=None, state=imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
    # Only loads image if the image is already opened, otherwise it returns a false flag for downstream to deal with
    def loadState(self,state):
        self.state = state
        return self.state[imageStateTraits.IMAGE_OPENED]
    # Only saves config if the image is already opened, otherwise it returns a false flag for downstream to deal with
    def saveState(self):
        return self.state[imageStateTraits.IMAGE_OPENED]
    # This sets the state back to the default
    def reset(self):
        self.state=imageState.copy()