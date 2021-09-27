import os
import cv2 as cv
import segmentImage as sI
import matplotlib.pyplot as plt
import tree
import walkTree

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
box = tree.Rectangle(0,0,image.shape[0],image.shape[1])
#Puts Cutoff length in format of tree cutoffThreshold
upperCutoff = upperCutoffDistance/image.shape[1]
#Creates Tree
root = tree.treeNode(box,list(cells),upperCutoff)

#Finds neighbors of cells using tree structure
#TODO:: Have root passed. Will not work when I move this code out of tree.py
walkTree.findCloseCells(root,cells,deviation,maxNeighborDistance)

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