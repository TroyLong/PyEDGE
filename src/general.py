#TODO:: I need to think about whether I should use the tree after getting an intial guess.
#       It could be creating more overhead than I want.
#       If I stop using the tree, are there any non n^2 algorithms to process my data.


import os
import cv2 as cv
import segmentImage as sI
import matplotlib.pyplot as plt
import tree
import walkTree
from cell import cellTraits as ct
import neighborFilters as nf
import mergeSort as ms
from math import dist
import numpy as np

#How far can a center be away from the last center and be in the same set
deviation = 15
#Sets a longest possible neighbor distance. Really important variable
maxNeighborDistance = 80000
#Allows a first order approximation to speed up tree branching. Small numbers don't look far enough, large numbers take a long time
upperCutoffDistance = 5000

#Loads image
imageDir = "SampleImages/"
imageName = "spidergfpapril12_11_z01_t021.tif"
imagePath = os.path.join(imageDir,imageName)
cells,image = sI.segmentImage(imagePath)

#This box is the default for the tree geometry
box = tree.Rectangle(0,0,image.shape[0],image.shape[1])
#Puts Cutoff length in format of tree cutoffThreshold
upperCutoff = image.shape[1]/upperCutoffDistance
#Creates Tree
root = tree.treeNode(box,list(cells),upperCutoff)

#Finds neighbors of cells using tree structure
walkTree.findCloseCells(root,cells)

nf.distanceFilter(cells,deviation)
nf.passThroughMultipleAreasFilter(cells,image)
#nf.oneToOneFilter(cells)


#This Draws the lines neighboring cells
for cell in cells:
    cv.circle(image, (cell[ct.CENTER][0],cell[ct.CENTER][1]), int(cell[ct.RADIUS]), (255, 255, 0), 2)
for cell in cells:
    for neighbor in cell[ct.NEIGHBORS]:
        cv.line(image,cell[ct.CENTER],neighbor[ct.CENTER],(132,124,255), 2)

#This converts the image to the same color format as pyplot.
image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
#Displays image with all alterations applied
plt.imshow(image)
plt.show()