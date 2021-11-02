import tkinter as tk
import cv2 as cv
import segmentImage as sI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import tree
import walkTree
from cell import cellTraits as ct
import neighborFilters as nf


class GraphFrame(tk.Frame):
    def __init__(self, master=None,deviation=0,maxNeighborDistance=0,upperCutoffDistance=0):
        super().__init__(master)
        self.master = master
        self.deviation = deviation
        self.maxNeighborDistance = maxNeighborDistance
        self.upperCutoffDistance = upperCutoffDistance
        self.__createGraphs()

    def resetImage(self,imagePath):
        self.imagePath = imagePath
        self.__runImageAnalysis()
        self.__setImages()
        self.__setGraphs()

    def __createGraphs(self):
        #Original Image
        #Unaltered Image from file
        self.originalImageLabel = tk.Label(self,text="Original")
        self.originalImageLabel.grid(row=0,column=0)
        self.originalImageFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        self.originalImageCanvas = FigureCanvasTkAgg(self.originalImageFig,self)
        self.originalImageCanvas.get_tk_widget().grid(row=1,column=0)
        #Toolbar has to go in Frame to back with grid
        originalImageToolbarFrame = tk.Frame(self)
        originalImageToolbarFrame.grid(row=2,column=0)
        originalImageToolbar = NavigationToolbar2Tk(self.originalImageCanvas,originalImageToolbarFrame)

        #Filtered Image
        #Image after going through openCV filters
        self.filteredImageLabel = tk.Label(self,text="Filtered")
        self.filteredImageLabel.grid(row=0,column=1)
        self.filteredImageFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        self.filteredImageCanvas = FigureCanvasTkAgg(self.filteredImageFig,self)
        self.filteredImageCanvas.get_tk_widget().grid(row=1,column=1)
        #Toolbar has to go in Frame to back with grid 
        filteredImageToolbarFrame = tk.Frame(self)
        filteredImageToolbarFrame.grid(row=2,column=1)
        filteredImageToolbar = NavigationToolbar2Tk(self.filteredImageCanvas,filteredImageToolbarFrame)

        #Neighbor Image
        #Drawings of the neighborhood paths
        self.neighborImageLabel = tk.Label(self,text="Neighbor Mapping")
        self.neighborImageLabel.grid(row=0,column=2)
        self.neighborImageFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        self.neighborImageCanvas = FigureCanvasTkAgg(self.neighborImageFig,self)
        self.neighborImageCanvas.get_tk_widget().grid(row=1,column=2)
        #Toolbar has to go in Frame to back with grid
        neighborImageToolbarFrame = tk.Frame(self)
        neighborImageToolbarFrame.grid(row=2,column=2)
        neighborImageToolbar = NavigationToolbar2Tk(self.neighborImageCanvas,neighborImageToolbarFrame)

        #Histogram of the neighborhood paths
        self.neighborHistLabel = tk.Label(self,text="Histogram of Neighbors")
        self.neighborHistLabel.grid(row=0,column=3)
        self.neighborHistFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        self.neighborHistCanvas = FigureCanvasTkAgg(self.neighborHistFig,self)
        self.neighborHistCanvas.get_tk_widget().grid(row=1,column=3)


    def __setGraphs(self):
        neighborNumbers = list()
        for cell in self.cells:
            neighborNumbers.append(len(cell[ct.NEIGHBORS]))
        self.neighborHistFig.clf()
        self.neighborHistPlt = self.neighborHistFig.add_subplot(111)        
        self.neighborHistPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
        self.neighborHistCanvas.draw()


    def __setImages(self):
        #Original Image
        self.originalImageFig.clf()
        self.originalImagePlt = self.originalImageFig.add_subplot(111)
        self.originalImagePlt.imshow(cv.cvtColor(cv.imread(self.imagePath),cv.COLOR_BGR2RGB))
        #Filtered Image
        self.filteredImageFig.clf()
        self.filteredImagePlt = self.filteredImageFig.add_subplot(111)
        self.filteredImagePlt.imshow(cv.cvtColor(self.filteredImage,cv.COLOR_BGR2RGB))
        #Neighbor Image
        self.neighborImageFig.clf()
        self.neighborImagePlt = self.neighborImageFig.add_subplot(111)        
        self.neighborImagePlt.imshow(cv.cvtColor(self.filteredImage,cv.COLOR_BGR2RGB))
        #Updates the canvas
        self.originalImageCanvas.draw()
        self.filteredImageCanvas.draw()
        self.neighborImageCanvas.draw()


    def __runImageAnalysis(self):
        self.cells,self.filteredImage = sI.segmentImage(self.imagePath)
        self.__runTreeApprox()
        self.__runNeighborFilters()
        self.__drawNeighborAnalysis()
    
    def __runTreeApprox(self):
        #This box is the default for the tree geometry
        box = tree.Rectangle(0,0,self.filteredImage.shape[0],self.filteredImage.shape[1])
        #Puts Cutoff length in format of tree cutoffThreshold
        upperCutoff = self.filteredImage.shape[1]/self.upperCutoffDistance
        #Creates Tree
        root = tree.treeNode(box,list(self.cells),upperCutoff)
        #Finds neighbors of cells using tree structure
        walkTree.findCloseCells(root,self.cells)
    
    def __runNeighborFilters(self):
        nf.distanceFilter(self.cells,self.deviation)
        nf.passThroughMultipleAreasFilter(self.cells,self.filteredImage)
    
    def __drawNeighborAnalysis(self):
        for cell in self.cells:
            cv.circle(self.filteredImage, (cell[ct.CENTER][0],cell[ct.CENTER][1]), int(cell[ct.RADIUS]), (255, 255, 0), 2)
            for neighbor in cell[ct.NEIGHBORS]:
                cv.line(self.filteredImage,cell[ct.CENTER],neighbor[ct.CENTER],(132,124,255), 2)