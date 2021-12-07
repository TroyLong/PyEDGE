# TODO:: Merge with tree.py
########################
##        About       ##
########################
# Used to navigate tree.py for the barnes--hut simulation
# Is currently seprate from tree.py for obsolete reasons
########################
## Imported Libraries ##
########################
# Neighbor Libraries
import tree
########################
## Internal Libraries ##
########################
# Neighbor Libraries
import cell as ce

# This correctly navigates the tree structure. Uses nodes that need to be used, and ignores decendants of those that don't
def findCloseCells(root,cells):
    for cell in cells:
        nodeIterator = tree.PreOrderIter(root)
        # Start looking through all nodes. Skip child nodes is parent node is past the cutoff
        for node in nodeIterator:
            # Is the node within the cutoff, not itself, and a cell? Then do action relevant action on node
            if (node.isNodeSingleOccupied and (not node.cells[0][ce.cellTraits.CENTER] == cell[ce.cellTraits.CENTER]) and (node.isInternalNodeWithinCutoff(cell))):
                node.findNeighborDistances(cell)
            # If the center of mass is out of the cutoff, then skip the nodes that are deeper
            elif not node.isInternalNodeWithinCutoff(cell):
                for i in range(len(node.descendants)):
                    next(nodeIterator, None)
        