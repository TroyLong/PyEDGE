########################
##        About       ##
########################
# Desides if two cells are neighbors based on a series of tests
# Split from neighborFilters.py because they are dealing with the data in completely different ways
########################
## Imported Libraries ##
########################
import cv2 as cv
from analysis.filters.neighborFilters.oneToOneFilter import oneToOneFilter
########################
## Internal Libraries ##
########################
import dataTypes.imageState as iS
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT
from dataTypes.dataTypeTraits import imageStateTraits as iST
from analysis.filters.neighborFilters.tooFewNeighborsFilter import tooFewNeighborsFilter
from analysis.filters.neighborFilters.distanceFilter import distanceFilter
from analysis.filters.neighborFilters.passThroughMultipleAreasFilter import passThroughMultipleAreasFilter
from . import walkTree as walkTree
from . import tree as tree
import analysis.cleanNeighbors as cN


## Only run through __createNeighborImage in graphFrame.py or another simular function. NEVER ON ITS OWN!!!
    
def processNeighborAnalysis(state):
    runTreeApprox(state)
    runNeighborFilters(state)
    drawNeighborAnalysis(state)



## Only run below functions through processNeighborAnalysis()

# Saves time by not considering neighbors to far away. Should run in O(nlg(n)) if set up correctly.
# Not sure if currently set up correctly (its been a while since I've looked).
def runTreeApprox(state):
    #This box is the default for the tree geometry
    box = tree.Rectangle(0,0,state.neighbor_image.shape[0],state.neighbor_image.shape[1])
    #Puts Cutoff length in format of tree cutoffThreshold
    upperCutoff = state.neighbor_image.shape[1]/state.upper_cutoff_dist
    #Creates Tree
    root = tree.treeNode(box,list(state.cells),upperCutoff)
    #Finds neighbors of cells using tree structure
    state.cells = walkTree.findCloseCells(root,state.cells)


# Knowingly breaks functional programming here
# This reduces the list of possible neighbors by throwing out neighbors that don't pass a series of tests
def runNeighborFilters(state):
    # TODO:: Neighbor lines are still drawing to these?
    # I think it is because the other cells still think it is a neighbor 
    # It is going to need a way to check if the neighbor still exists afterwords
    # Running recursively should get rid of chaining effects.
    state.cells = distanceFilter(state,state.deviation)
    state.cells = tooFewNeighborsFilter(state,2)
    #state[iST.CELLS] = oneToOneFilter(state)
    #state[iST.CELLS] = passThroughMultipleAreasFilter(state)
    
    
    
# This draws the neighbor lines and the circles on the neighbor image
def drawNeighborAnalysis(state):
    for cell in state.cells:
        cv.circle(state.neighbor_image, (cell[cT.CENTER][0],cell[cT.CENTER][1]), int(cell[cT.RADIUS]), (255, 255, 0), 2)
        for neighbor in cell[cT.NEIGHBORS]:
            cv.line(state.neighbor_image,cell[cT.CENTER],neighbor[cNT.CELL][cT.CENTER],(132,124,255), 2)