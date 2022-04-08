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
from analysis.filters.neighborFilters.tooFewNeighborsFilter import too_few_neighbors_filter
from analysis.filters.neighborFilters.distanceFilter import distance_filter
from analysis.filters.neighborFilters.passThroughMultipleAreasFilter import pass_through_multiple_areas_filter
from . import walkTree as walkTree
from . import tree as tree


## Only run through __createNeighborImage in graphFrame.py or another simular function. NEVER ON ITS OWN!!!
    
def process_neighbor_analysis(state):
    run_tree_approx(state)
    run_neighbor_filters(state)
    draw_neighbor_analysis(state)

## Only run below functions through process_neighbor_analysis()

# Saves time by not considering neighbors to far away. Should run in O(nlg(n)) if set up correctly.
# Not sure if currently set up correctly (its been a while since I've looked).
def run_tree_approx(state):
    #This box is the default for the tree geometry
    tree_root = tree.Rectangle(0,0,state.neighbor_image.shape[0],state.neighbor_image.shape[1])
    #Puts Cutoff length in format of tree cutoffThreshold
    upper_cutoff = state.neighbor_image.shape[1]/state.upper_cutoff_dist
    #Creates Tree
    root = tree.TreeNode(tree_root,list(state.cells),upper_cutoff)
    #Finds neighbors of cells using tree structure
    state.cells = walkTree.find_close_cells(root,state.cells)

# Knowingly breaks functional programming here
# This reduces the list of possible neighbors by throwing out neighbors that don't pass a series of tests
def run_neighbor_filters(state):
    state.cells = distance_filter(state,state.deviation)
    state.clean_neighbors()
    state.cells = too_few_neighbors_filter(state,2)
    state.clean_neighbors()
    state.cells = pass_through_multiple_areas_filter(state)
    state.clean_neighbors()
     
# This draws the neighbor lines and the circles on the neighbor image
def draw_neighbor_analysis(state):
    for cell in state.cells:
        cv.circle(state.neighbor_image, (cell.center[0],cell.center[1]), int(cell.radius), (255, 255, 0), 2)
        for neighbor in cell.neighbors:
            cv.line(state.neighbor_image,cell.center,neighbor.cell.center,(132,124,255), 2)