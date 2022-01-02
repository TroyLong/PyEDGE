# TODO:: Merge with tree.py
########################
##        About       ##
########################
# Used to navigate tree.py for the barnes--hut simulation
# Is currently seprate from tree.py for obsolete reasons
########################
## Internal Libraries ##
########################
import dataTypes.cell as ce
from dataTypes.cell import cellTraits as cT
from . import tree as tree


# Functional Form
# This correctly navigates the tree structure. Uses nodes that need to be used, and ignores decendants of those that don't
def findCloseCells(root,cells):
    # Builds functional form output
    tempCells = list()
    for cell in cells:
        # Prevents accidental overwrite of cell
        cell = cell.copy()
        # List fills as neighbors are found
        tempNeighbors = list()
        # Turns the nodes into an iteration, which Python enjoys
        nodeIterator = tree.PreOrderIter(root)
        # Start looking through all nodes. Skip child nodes is parent node is past the cutoff
        for node in nodeIterator:
            # Is the node within the cutoff, not itself, and a cell? Then do action relevant action on node
            if (node.isNodeSingleOccupied and (not node.cells[0][ce.cellTraits.CENTER] == cell[ce.cellTraits.CENTER]) and (node.isInternalNodeWithinCutoff(cell))):
                # If plausable neighbors, then append to neighbor list
                tempNeighbors.append(node.buildNeighborCell(cell))
            # If the center of mass is out of the cutoff, then skip the nodes that are deeper
            elif not node.isInternalNodeWithinCutoff(cell):
                for i in range(len(node.descendants)):
                    next(nodeIterator, None)
        # Remember this is just a copy of the original cell
        cell[cT.NEIGHBORS] = tuple(tempNeighbors)
        # This adds this cell and its neighbors to the total cells collection
        tempCells.append(cell)
    # Returns new data structure
    return tempCells
        