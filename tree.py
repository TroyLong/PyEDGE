# This is a Barnes-Hut Tree. It might be used for neighborhood estimation if this makes it any faster.
# It also might be used to compare the closeness to estimations across multiple images
from math import dist
from scipy import constants
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2 as cv
import segmentImage as sI

from anytree import NodeMixin, RenderTree, PreOrderIter


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



#This is the node to the Barnes-Hut tree structure
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
        self.parentCutoff = True
        self.childRects = []
        self.childcellPartitions = [[],[],[],[]]
        if children:
            self.children = children
        if len(cells) > 0:
            self.__findCenterOfMass()
        if len(cells) > 1:
            self.__createChildrenNodes()
        # Does this node have only 1 element?
        self.isNodeOccupied = len(cells) > 0
    def setSerial(self):
        global Serial
        self.Serial = Serial
        Serial += 1

    def update(self,cell):
        if(self.is_leaf and self.isNodeOccupied):
            pass     
    # Is cell far enough away to be considered seprate
    def isInternalNodeWithinCutoff(self,cell):
        cellToNode = np.sqrt((cell["center"][0]-self.centerOfMass[0])**2+(cell["center"][1]-self.centerOfMass[1])**2)
        cellToNode = cellToNode if cellToNode != 0 else 0.000000001
        sd = self.rect.width/cellToNode
        return  sd <= self.cutoffThreshold

    def __findCenterOfMass(self):
        self.totalArea = 0
        for cell in self.cells:
            self.centerOfMass[0] += cell["area"]*cell["center"][0]
            self.centerOfMass[1] += cell["area"]*cell["center"][1]
            self.totalArea += cell["area"]
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
                if ((cell["center"][0] >= self.childRects[i].x)
                        and (cell["center"][0] < (self.childRects[i].x+self.childRects[i].width))
                        and (cell["center"][1] >= self.childRects[i].y)
                        and (cell["center"][1] < (self.childRects[i].y+self.childRects[i].height))):
                    self.childcellPartitions[i].append(cell)
                    self.cells.remove(cell)





def findCloseCells(cells):
    for cell in cells:
        nodeIterator = PreOrderIter(root)
        # Start looking through all nodes. Skip child nodes is parent node is past the cutoff
        for node in nodeIterator:
            # Is the center of mass of the node within the cutoff, if so, continue searching deeper
            if (node.is_leaf and node.isNodeOccupied and (not node.cells[0] == cell) and (node.isInternalNodeWithinCutoff(cell))):
                print("Update {0}".format(cell.Serial))
                node.update(cell)
            # Check if the cell is checking itself against itself
            elif node.is_leaf and node.isNodeOccupied and (node.cells[0] == cell):
                print('Self')
                pass
            # If the center of mass is out of the cutoff, make approximation, and skip the nodes that are deeper
            elif not node.isInternalNodeWithinCutoff(cell):
                print("Not within Cutoff?")
                node.update(cell)
                # Skip all descendants of current node
                for i in range(len(node.descendants)):
                    next(nodeIterator, None)
        cell.update(.001)


imageDir = "SampleImages/"
imageName = "spidergfpapril12_11_z01_t021.tif"
imagePath = os.path.join(imageDir,imageName)
cells,image = sI.segmentImage(imagePath)
ncells = len(cells)
box = Rectangle(0,0,10,10)
root = treeNode(box,list(cells),500000)

image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
plt.imshow(image)
plt.show()



xaxis = [[],[],[],[]]
yaxis = [[],[],[],[]]

###
#for i in range(ncells):
#    for i in range(ncells):
#        xaxis[i].append(cells[i]["center"][0])
#        yaxis[i].append(cells[i]["center"][1])
#    findCloseCells(cells)
#    root = treeNode(box,list(cells),5000)
#
#for i in range(ncells):
#    plt.scatter(xaxis[i],yaxis[i])
#
#plt.show()
###