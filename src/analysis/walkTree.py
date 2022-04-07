########################
##        About       ##
########################
# Used to navigate tree.py for the barnes--hut simulation
# Is currently seprate from tree.py because this is a stand alone function right now, while tree is full
# Of more OOP structures. They might become merged, but not right now.
########################
## Internal Libraries ##
########################
from . import tree as tree
import copy

# Functional Form
# This correctly navigates the tree structure. Uses nodes that need to be used, and ignores decendants of those that don't
def findCloseCells(root,cells):
    # Builds functional form output
    tempCells = list()
    for cell in cells:
        # Prevents accidental overwrite of cell
        # TODO:: Should this be copy or deep copy?
        cell = copy.copy(cell)
        # List fills as neighbors are found
        tempNeighbors = list()
        # Turns the nodes into an iteration, which Python enjoys
        nodeIterator = tree.PreOrderIter(root)
        # Start looking through all nodes. Skip child nodes is parent node is past the cutoff
        for node in nodeIterator:
            # Is the node within the cutoff, not itself, and a cell? Then do action relevant action on node
            if (node.isNodeSingleOccupied and (not node.cells[0].center == cell.center) and (node.isInternalNodeWithinCutoff(cell))):
                # If plausable neighbors, then append to neighbor list
                tempNeighbors.append(node.buildNeighborCell(cell))
            # If the center of mass is out of the cutoff, then skip the nodes that are deeper
            elif not node.isInternalNodeWithinCutoff(cell):
                for i in range(len(node.descendants)):
                    next(nodeIterator, None)
        # Remember this is just a copy of the original cell
        cell.neighbors = tuple(tempNeighbors)
        # This adds this cell and its neighbors to the total cells collection
        tempCells.append(cell)
    # Returns new data structure
    return tempCells
        