########################
##        About       ##
########################
# This holds the state information for each image loaded into the main program
########################
## Imported Libraries ##
########################
import numpy as np
########################
## Internal Libraries ##
########################
from dataTypes.imageStateTraits import imageStateTraits as iST
from dataTypes.cell import cellTraits as cT


# Provides a basic empty image for the default state
emptyImage = np.zeros(np.shape([1,1,3]),dtype=np.uint8)



# A dictionary is used over a traditional object for speed
imageState = {iST.IMAGE_OPENED:False,
                iST.IMAGE:emptyImage.copy(),iST.FILTERED_IMAGE:emptyImage.copy(),
                iST.NEIGHBOR_IMAGE:emptyImage.copy(),
                iST.CELLS:tuple(),iST.CELL_INDEX:0,
                iST.MEAN_CELL_RADII:0,
                iST.FILTER_DIAMETER:1,iST.SIGMA_COLOR:0,
                iST.SIGMA_SPACE:0,iST.ADAPTIVE_BLOCKSIZE:3,
                iST.DEVIATION:15.0,iST.MAX_NEIGHBHOR_DIST:80000.0,
                iST.UPPER_CUTOFF_DIST:5000.0}


# Functions on imageState data structure ############

# Finds the mean radii of all the cells in a state
def meanCellRadii(state):
    averageRadius = 0
    for cell in state[iST.CELLS]:
        averageRadius += cell[cT.RADIUS]
    try:
        return averageRadius/(len(state[iST.CELLS]))
    except ZeroDivisionError:
        return 0

# Caluclates the deviation in cell radii
# There is probably also a library for this
def cellRadiusDeviation(state):
    deviation = 0
    meanRadius = meanCellRadii(state)
    for cell in state[iST.CELLS]:
        deviation += (cell[cT.RADIUS]-meanRadius)**2
    try:
        return np.sqrt(deviation/(len(state[iST.CELLS])))
    except ZeroDivisionError:
        return 0

# Debug tool that prints state in a readable format
def printState(imgState):
    print("  \n######  STATE PRINTOUT  ######"
            "\nImage Created:         " + str(imgState[iST.IMAGE_OPENED]) +
            "\n######  Filter Options  ######" +
            "\nFilter Diameter:       " + str(imgState[iST.FILTER_DIAMETER]) +
            "\nSigma Color:           " + str(imgState[iST.SIGMA_COLOR]) +
            "\nSimga Space:           " + str(imgState[iST.SIGMA_SPACE]) +
            "\nAdaptive Blocksize:    " + str(imgState[iST.ADAPTIVE_BLOCKSIZE]) +
            "\n######  Neighbor Options #####" +
            "\nDeviation:             " + str(imgState[iST.DEVIATION]) + 
            "\nMax Neighbor Distance: " + str(imgState[iST.MAX_NEIGHBHOR_DIST]) +
            "\nUpper Cutoff Distance: " + str(imgState[iST.UPPER_CUTOFF_DIST]) +
            "\n\n")


