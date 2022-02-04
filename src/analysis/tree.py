########################
##        About       ##
########################
# This is a Barnes-Hut Tree. It might be used for neighborhood estimation if this makes it any faster.
# It also might be used to compare the closeness to estimations across multiple images
########################
## Imported Libraries ##
########################
from math import dist
import numpy as np
from anytree import NodeMixin, PreOrderIter
########################
## Internal Libraries ##
########################
import dataTypes.cell as ce
import dataTypes.cellNeighbor as cN
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import cellNeighborTraits as cNT

Serial = 0
BodySerial = 0



# This is a rectangle object that also keeps up with its bisections
class Rectangle(object):
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.midX = x + (width / 2)
        self.midY = y + (height / 2)
    # Checks if a given position falls inside the rectangle
    def isPositionInside(self,position):
        if ((self.x <= position[0]) and (self.x+self.width > position[0])
            and (self.y <= position[1]) and (self.y+self.height > position[1])):
            return True
        return False



#TODO:: Recomment this section to be clearer to the new purpose of this code
#This is the node to the Barnes-Hut tree structure. It was recycled from my n-body simulator.
class treeNode(NodeMixin):
    def __init__(self,rect,cells=[],cutoffThreshold = 0,parent=None,children=None):
        # each node is serialized for easy naming scheme
        self.setSerial()
        #this the area under the control of the node
        self.rect = rect
        self.parent = parent
        #this is all of the cells in the node. The lowest node doesn
        self.cells = cells
        self.totalArea = 0
        self.centerOfMass = [0,0]
        self.cutoffThreshold = cutoffThreshold
        #temp variable
        self.childRects = []
        self.childcellPartitions = [[],[],[],[]]
        if children:
            self.children = children
        if len(cells) > 0:
            self.__findCenterOfMass()
        if len(cells) > 1:
            self.__createChildrenNodes()
        # Does this node have only 1 element?
        self.isNodeSingleOccupied = len(cells) == 1
    def setSerial(self):
        global Serial
        self.Serial = Serial
        Serial += 1


    # Functional Form
    # This should be more related to cellDist
    # Finds distances to neighbors and cell area for initial guess
    def buildNeighborCell(self,cell):
        if(self.isNodeSingleOccupied):
            neighborCell = cN.cellNeighbor.copy()
            neighborCell[cNT.CELL] = self.cells[0]
            neighborCell[cNT.DISTANCE_TO_BORDER] = self._neighborCellDistanceToBorder(cell)
            return neighborCell
    def _neighborCellDistanceToBorder(self,cell):
        return ce.cellDist(cell,self.cells[0])-cell[cT.RADIUS]


    # Is cell far enough away to be considered seprate
    def isInternalNodeWithinCutoff(self,cell):
        cellToNode = np.sqrt((cell[cT.CENTER][0]-self.centerOfMass[0])**2+(cell[cT.CENTER][1]-self.centerOfMass[1])**2)
        cellToNode = cellToNode if cellToNode != 0 else 0.000000001
        sd = self.rect.width/cellToNode
        return  sd >= self.cutoffThreshold

    def __findCenterOfMass(self):
        self.totalArea = 0
        for cell in self.cells:
            self.centerOfMass[0] += cell[cT.AREA]*cell[cT.CENTER][0]
            self.centerOfMass[1] += cell[cT.AREA]*cell[cT.CENTER][1]
            self.totalArea += cell[cT.AREA]
        if self.totalArea == 0:
            self.totalArea = 0.000000001
        self.centerOfMass[0] /= self.totalArea
        self.centerOfMass[1] /= self.totalArea

    def __createChildrenNodes(self):
        self.__createChildRectangles()
        self.__subdividecells()
        self.children = list()
        for i in range(4):
            treeNode(self.childRects[i],self.childcellPartitions[i],self.cutoffThreshold).parent = self
    def __createChildRectangles(self):
        newHeight, newWidth = self.rect.height/2, self.rect.width/2
        self.childRects = [Rectangle(self.rect.x,self.rect.y,newHeight,newWidth),
                            Rectangle(self.rect.midX,self.rect.y,newHeight,newWidth),
                            Rectangle(self.rect.x,self.rect.midY,newHeight,newWidth),
                            Rectangle(self.rect.midX,self.rect.midY,newHeight,newWidth)]
    def __subdividecells(self):
        for cell in list(self.cells):
            for i in range(len(self.childRects)):
                #which the cell in the childRect being checked
                if ((cell[cT.CENTER][0] >= self.childRects[i].x)
                        and (cell[cT.CENTER][0] < (self.childRects[i].x+self.childRects[i].width))
                        and (cell[cT.CENTER][1] >= self.childRects[i].y)
                        and (cell[cT.CENTER][1] < (self.childRects[i].y+self.childRects[i].height))):
                    self.childcellPartitions[i].append(cell)
                    self.cells.remove(cell)