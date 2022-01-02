########################
##        About       ##
########################
# Desides if two cells are neighbors based on a series of tests
# Split from neighborFilters.py because they are dealing with the data in completely different ways
########################
## Imported Libraries ##
########################
import cv2 as cv
########################
## Internal Libraries ##
########################
from dataTypes.cell import cellTraits as ct
from dataTypes.cellNeighbor import cellNeighborTraits as cnt
import dataTypes.imageState as iS
from dataTypes.imageStateTraits import imageStateTraits as iST
from analysis.filters.neighborFilters.tooFewNeighborsFilter import tooFewNeighborsFilter
from analysis.filters.neighborFilters.distanceFilter import distanceFilter
from analysis.filters.neighborFilters.passThroughMultipleAreasFilter import passThroughMultipleAreasFilter
from . import walkTree as walkTree
from . import tree as tree



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
    box = tree.Rectangle(0,0,state[iST.NEIGHBOR_IMAGE].shape[0],state[iST.NEIGHBOR_IMAGE].shape[1])
    #Puts Cutoff length in format of tree cutoffThreshold
    upperCutoff = state[iST.NEIGHBOR_IMAGE].shape[1]/state[iST.UPPER_CUTOFF_DIST]
    #Creates Tree
    root = tree.treeNode(box,list(state[iST.CELLS]),upperCutoff)
    #Finds neighbors of cells using tree structure
    state[iST.CELLS] = walkTree.findCloseCells(root,state[iST.CELLS])


# Knowingly breaks functional programming here
# This reduces the list of possible neighbors by throwing out neighbors that don't pass a series of tests
def runNeighborFilters(state):
    state[iST.CELLS] = distanceFilter(state,state[iST.DEVIATION])
    # TODO:: Neighbor lines are still drawing to these?
    # I think it is because the other cells still think it is a neighbor 
    # It is going to need a way to check if the neighbor still exists afterwords
    # Running recursively should get rid of chaining effects.
    state[iST.CELLS] = tooFewNeighborsFilter(state,1)
    state[iST.CELLS] = passThroughMultipleAreasFilter(state)
    
    
    
# This draws the neighbor lines and the circles on the neighbor image
def drawNeighborAnalysis(state):
    for cell in state[iST.CELLS]:
        cv.circle(state[iST.NEIGHBOR_IMAGE], (cell[ct.CENTER][0],cell[ct.CENTER][1]), int(cell[ct.RADIUS]), (255, 255, 0), 2)
        for neighbor in cell[ct.NEIGHBORS]:
            cv.line(state[iST.NEIGHBOR_IMAGE],cell[ct.CENTER],neighbor[cnt.CELL][ct.CENTER],(132,124,255), 2)