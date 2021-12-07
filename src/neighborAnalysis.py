########################
##        About       ##
########################
# Desides if two cells are neighbors based on a series of tests
# Split from neighborFilters.py because they are dealing with the data in completely different ways
########################
## Imported Libraries ##
########################
# Image Analysis Libraries
import cv2 as cv
# Neighbor Libraries
import tree
########################
## Internal Libraries ##
########################
# Neighbor Libraires
from cell import cellTraits as ct
import neighborFilters as nf
import walkTree
# State Machine Libraries
import imageState as iS
from imageState import imageStateTraits as iST


# Should only run within __createNeighborImage in graphFrame.py or another simular function. NEVER ON ITS OWN!!!
    
def processNeighorAnalysis(state):
    runTreeApprox(state)
    runNeighborFilters(state)
    drawNeighborAnalysis(state)

# Should not run without processNeighborAnalysis()
def runTreeApprox(state):
    #This box is the default for the tree geometry
    box = tree.Rectangle(0,0,state[iST.NEIGHBOR_IMAGE].shape[0],state[iST.NEIGHBOR_IMAGE].shape[1])
    #Puts Cutoff length in format of tree cutoffThreshold
    upperCutoff = state[iST.NEIGHBOR_IMAGE].shape[1]/state[iST.UPPER_CUTOFF_DIST]
    #Creates Tree
    root = tree.treeNode(box,list(state[iST.CELLS]),upperCutoff)
    #Finds neighbors of cells using tree structure
    walkTree.findCloseCells(root,state[iST.CELLS])
def runNeighborFilters(state):
    nf.distanceFilter(state[iST.CELLS],state[iST.DEVIATION])
    nf.passThroughMultipleAreasFilter(state[iST.CELLS],state[iST.NEIGHBOR_IMAGE])
def drawNeighborAnalysis(state):
    for cell in state[iST.CELLS]:
        cv.circle(state[iST.NEIGHBOR_IMAGE], (cell[ct.CENTER][0],cell[ct.CENTER][1]), int(cell[ct.RADIUS]), (255, 255, 0), 2)
        for neighbor in cell[ct.NEIGHBORS]:
            cv.line(state[iST.NEIGHBOR_IMAGE],cell[ct.CENTER],neighbor[ct.CENTER],(132,124,255), 2)