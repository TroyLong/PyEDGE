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
# This correctly navigates the tree structure. Uses nodes that need to be used, and ignores descendants of those that don't
def findCloseCells(root,cells):
    temp_cells = list()
    for cell in cells:
        neighbors = list()
        node_iterator = tree.PreOrderIter(root)
        # Skip child nodes is parent node is past the cutoff
        for node in node_iterator:
            # Is the node within the cutoff, not itself, and a cell? Then do action relevant action on node
            if (node.isNodeSingleOccupied and (not node.cells[0].center == cell.center) and (node.isInternalNodeWithinCutoff(cell))):
                # If plausable neighbors, then append to neighbor list
                neighbors.append(node.buildNeighborCell(cell))
            # If the center of mass is out of the cutoff, then skip the nodes that are deeper
            elif not node.isInternalNodeWithinCutoff(cell):
                for i in range(len(node.descendants)):
                    next(node_iterator, None)
        # Remember this is just a copy of the original cell
        cell.neighbors = tuple(neighbors)
        # This adds this cell and its neighbors to the total cells collection
        temp_cells.append(cell)
    # Returns new data structure
    return tuple(temp_cells)
        