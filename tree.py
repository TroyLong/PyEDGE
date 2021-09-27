# This is a Barnes-Hut Tree. It might be used for neighborhood estimation if this makes it any faster.
# It also might be used to compare the closeness to estimations across multiple images
from math import dist
from scipy import constants
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2 as cv
import segmentImage as sI
import sorting as srt

from anytree import NodeMixin, RenderTree, PreOrderIter
from enum import Enum

Serial = 0
BodySerial = 0



#TODO:: Find one that already exists, get rid of it, or add it to a file of convienent functions
#TODO:: If I commit to this function, then I need to actually use it where it is needed
def pointsDist(pointA,pointB):
    return np.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)







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







#TODO:: Figure out if the cutoffThreshold is working as it should. I think it might be being ignored on empty parent nodes.
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
        self.isNodeSingleOccupied = len(cells) == 1
    def setSerial(self):
        global Serial
        self.Serial = Serial
        Serial += 1

    #TODO:: Walk through this only once for each cell, instead of twice
    # Finds distances to neighbors for initial guess
    def findNeighborDistances(self,cell):
        if(self.isNodeSingleOccupied):
            cell["neighborGuessDist"].append(pointsDist(cell["center"],self.centerOfMass))

    # Finds maximum distance for probable neighboring cells and resets the cutoffThreshold accordingly.
    def findMaxNeighborDistance(self,deviation):
        self.cells[0]["neighborGuessDist"] = srt.merge(self.cells[0]["neighborGuessDist"])
        try:
            maxDistance = self.cells[0]["neighborGuessDist"][0]
            for distance in range(1,len(self.cells[0]["neighborGuessDist"])):
                if (self.cells[0]["neighborGuessDist"][distance] < maxDistance+deviation):
                    maxDistance = self.cells[0]["neighborGuessDist"][distance]
                else:
                    break
            #TODO:: Make this work with the already present cutoff threshold
            self.cutoffThreshold = maxDistance/self.rect.width
        except IndexError:
            self.cutoffThreshold = 0


    def findNeighbors(self,cell,maxNeighborDistance):
        if(self.isNodeSingleOccupied and pointsDist(cell["center"],self.centerOfMass) <= maxNeighborDistance):
            self.cells[0]["neighbors"].append(cell["center"])

    # Is cell far enough away to be considered seprate
    def isInternalNodeWithinCutoff(self,cell):
        cellToNode = np.sqrt((cell["center"][0]-self.centerOfMass[0])**2+(cell["center"][1]-self.centerOfMass[1])**2)
        cellToNode = cellToNode if cellToNode != 0 else 0.000000001
        sd = cellToNode/self.rect.width
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







#TODO:: Put the below in their own file. The above is really all that should be in this one.
class treeUpdateActions(Enum):
    DISTANCES = 1
    MAX_DISTANCE = 2
    NEIGHBORS = 3







# This finds the neighbors using the moments of the cells
def findCloseCells(cells,deviation,maxNeighborDistance):
    # Finds the distance between all cells and all other cells within initial cutoff distances from each other.
    walkTree(cells,treeUpdateActions.DISTANCES)
    # Finds the largest distance around each cell from probable neighbors.
    walkTree(cells,treeUpdateActions.MAX_DISTANCE,deviation)
    # Finds probable neighbors for each cell.
    walkTree(cells,treeUpdateActions.NEIGHBORS,maxNeighborDistance=maxNeighborDistance)

# This correctly navigates the tree structure. Uses nodes that need to be used, and ignores decendants of those that don't
def walkTree(cells,updateAction,deviation=0,maxNeighborDistance=0):
    for cell in cells:
        nodeIterator = PreOrderIter(root)
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







#How far can a center be away from the last center and be in the same set
deviation = 15
#TODO:: I do not like this
maxNeighborDistance = 100
#TODO:: I think this needs work
# First over-estimated guess for cell neighbors
upperCutoffDistance = 5000

#Loads image
imageDir = "SampleImages/"
imageName = "spidergfpapril12_11_z01_t021.tif"
imagePath = os.path.join(imageDir,imageName)
cells,image = sI.segmentImage(imagePath)

#This box is the default for the tree geometry
box = Rectangle(0,0,image.shape[0],image.shape[1])
#Puts Cutoff length in format of tree cutoffThreshold
upperCutoff = upperCutoffDistance/image.shape[1]
#Creates Tree
root = treeNode(box,list(cells),upperCutoff)

#Finds neighbors of cells using tree structure
#TODO:: Have root passed. Will not work when I move this code out of tree.py
findCloseCells(cells,deviation,maxNeighborDistance)

#This Draws the lines neighboring cells
for cell in cells:
    cv.circle(image, (cell["center"][0],cell["center"][1]), 3, (255, 255, 0), -1)
    for neighbor in cell["neighbors"]:
        cv.line(image,cell["center"],neighbor,(132,124,255), 2)

#This converts the image to the same color format as pyplot.
image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
#Displays image with all alterations applied
plt.imshow(image)
plt.show()