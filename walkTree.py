from enum import Enum
import tree

class treeUpdateActions(Enum):
    DISTANCES = 1
    MAX_DISTANCE = 2
    NEIGHBORS = 3


# This finds the neighbors using the moments of the cells
def findCloseCells(root,cells,deviation,maxNeighborDistance):
    # Finds the distance between all cells and all other cells within initial cutoff distances from each other.
    walkTree(root,cells,treeUpdateActions.DISTANCES)
    # Finds the largest distance around each cell from probable neighbors.
    walkTree(root,cells,treeUpdateActions.MAX_DISTANCE,deviation)
    # Finds probable neighbors for each cell.
    walkTree(root,cells,treeUpdateActions.NEIGHBORS,maxNeighborDistance=maxNeighborDistance)

# This correctly navigates the tree structure. Uses nodes that need to be used, and ignores decendants of those that don't
def walkTree(root,cells,updateAction,deviation=0,maxNeighborDistance=0):
    for cell in cells:
        nodeIterator = tree.PreOrderIter(root)
        # Start looking through all nodes. Skip child nodes is parent node is past the cutoff
        for node in nodeIterator:
            # Is the node within the cutoff, not itself, and a cell? Then do action relevant action on node
            if (node.isNodeSingleOccupied and (not node.cells[0]["center"] == cell["center"]) and (node.isInternalNodeWithinCutoff(cell))):
                treeActions(node,cell,deviation,maxNeighborDistance,updateAction)
            # If the center of mass is out of the cutoff, then skip the nodes that are deeper
            elif not node.isInternalNodeWithinCutoff(cell):
                for i in range(len(node.descendants)):
                    next(nodeIterator, None)

# Actions taken by walkTree. Was created because this was origianlly called twice. Function calls are "slow", so it may go. But, it is convienent and modular
def treeActions(node,cell,deviation,maxNeighborDistance,updateAction):
    if (updateAction==treeUpdateActions.DISTANCES):
        node.findNeighborDistances(cell)
    elif (updateAction==treeUpdateActions.MAX_DISTANCE):
        node.findMaxNeighborDistance(deviation)
    elif (updateAction==treeUpdateActions.NEIGHBORS):
        node.findNeighbors(cell,maxNeighborDistance)