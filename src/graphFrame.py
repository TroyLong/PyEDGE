import tkinter as tk
import cv2 as cv
import segmentImage as sI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import tree
import walkTree
from cell import cellTraits as ct
from imageState import imageStateTraits as iST
import neighborFilters as nf
import imageState as iS


class GraphZoneFrame(tk.Frame):
    def __init__(self, master=None,state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
        self.__createGraphs()

    def loadState(self,state):
        self.state = state
        self.__loadImages()

    def openFile(self,imagePath):
        self.imagePath = imagePath
        self.__createOriginalImage()
        self.__createFilteredImageAndCells()
        self.__createNeighborImage()
        self.__loadImages()

    # These functions can be called to have images re-created
    def updateFilterOptions(self):
        self.__createFilteredImageAndCells()
        self.updateNeighborOptions()
    def updateNeighborOptions(self):
        self.__createNeighborImage()
        #TODO:: Do I still use these functions?
        self.__loadImages()
        self.__setGraphs()

    # These functions create the spaces where the images can be placed
    def __createGraphs(self):
        self.grid()
        self.__createOriginalGraph(0)
        self.__createFilteredGraph(1)
        self.__createNeighborGraph(2)
        self.__createNeighborHistogramGraph(3)
    def __createOriginalGraph(self,column):
        self.originalImageFrame = ImageFrame(self,state=self.state,imageType=iST.IMAGE,imageLabelText="Original")
        self.originalImageFrame.grid(row=1,column=column)
    def __createFilteredGraph(self,column):
        self.filteredImageFrame = ImageFrame(self,state=self.state,imageType=iST.FILTERED_IMAGE,imageLabelText="Filtered")
        self.filteredImageFrame.grid(row=1,column=column)
    def __createNeighborGraph(self,column):
        self.neighborImageFrame = ImageFrame(self,state=self.state,imageType=iST.NEIGHBOR_IMAGE,imageLabelText="Neighbor Mapping")
        self.neighborImageFrame.grid(row=1,column=column)
    def __createNeighborHistogramGraph(self,column):
        self.neighborHistFrame = HistFrame(self,state=self.state,imageLabelText="Neighbor Histogram")
        self.neighborHistFrame.grid(row=1,column=column)

    # These functions create and recreate the images loaded by the program
    def __createOriginalImage(self):
        self.state[iST.IMAGE] = cv.imread(self.imagePath)
    def __createFilteredImageAndCells(self):
        self.state[iST.CELLS],self.state[iST.FILTERED_IMAGE] = sI.segmentImage(self.state[iST.IMAGE])
    def __createNeighborImage(self):
        self.state[iST.NEIGHBOR_IMAGE] = self.state[iST.FILTERED_IMAGE].copy()    
        self.__processNeighorAnalysis()

    # Should only run within __createNeighborImage. NEVER ON ITS OWN!!!
    def __processNeighorAnalysis(self):
        self.__runTreeApprox()
        self.__runNeighborFilters()
        self.__drawNeighborAnalysis()
    def __runTreeApprox(self):
        #This box is the default for the tree geometry
        box = tree.Rectangle(0,0,self.state[iST.NEIGHBOR_IMAGE].shape[0],self.state[iST.NEIGHBOR_IMAGE].shape[1])
        #Puts Cutoff length in format of tree cutoffThreshold
        upperCutoff = self.state[iST.NEIGHBOR_IMAGE].shape[1]/self.state[iST.UPPER_CUTOFF_DIST]
        #Creates Tree
        root = tree.treeNode(box,list(self.state[iST.CELLS]),upperCutoff)
        #Finds neighbors of cells using tree structure
        walkTree.findCloseCells(root,self.state[iST.CELLS])
    def __runNeighborFilters(self):
        nf.distanceFilter(self.state[iST.CELLS],self.state[iST.DEVIATION])
        nf.passThroughMultipleAreasFilter(self.state[iST.CELLS],self.state[iST.NEIGHBOR_IMAGE])
    def __drawNeighborAnalysis(self):
        for cell in self.state[iST.CELLS]:
            cv.circle(self.state[iST.NEIGHBOR_IMAGE], (cell[ct.CENTER][0],cell[ct.CENTER][1]), int(cell[ct.RADIUS]), (255, 255, 0), 2)
            for neighbor in cell[ct.NEIGHBORS]:
                cv.line(self.state[iST.NEIGHBOR_IMAGE],cell[ct.CENTER],neighbor[ct.CENTER],(132,124,255), 2)

    # These functions load pre-created images to the graphs
    def __loadImages(self):
        self.__loadOriginalImage()
        self.__loadFilteredImage()
        self.__loadNeighborImage()
        self.__loadNeighborHist()
    def __loadOriginalImage(self):
        self.originalImageFrame.loadState(self.state)
    def __loadFilteredImage(self):
        self.filteredImageFrame.loadState(self.state)
    def __loadNeighborImage(self):       
        self.neighborImageFrame.loadState(self.state)
    def __loadNeighborHist(self):
        self.neighborHistFrame.loadState(self.state)





class ImageFrame(tk.Frame):
    def __init__(self, master=None,state=iS.imageState.copy(),imageType=None,imageLabelText = ""):
        super().__init__(master)
        self.master = master
        self.state = state
        self.imageLabelText = imageLabelText
        self.imageType = imageType
        self.__createImageLabel()
        self.__createImageFigure()
    
    def loadState(self,state):
        self.state = state
        self.__loadImageState()

    def __createImageLabel(self):
        self.graphLabel = tk.Label(self,text=self.imageLabelText)
        self.graphLabel.grid(row=0,column=0)
    def __createImageFigure(self):
        self.imageFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        # Canvas for the image or graph to display to
        self.imageCanvas = FigureCanvasTkAgg(self.imageFig,self)
        self.imageCanvas.get_tk_widget().grid(row=1,column=0)
        # Toolbar has to go in Frame to back with grid
        imageToolbarFrame = tk.Frame(self)
        imageToolbarFrame.grid(row=2,column=0)
        imageToolbar = NavigationToolbar2Tk(self.imageCanvas,imageToolbarFrame)

    def __loadImageState(self):
        self.imageFig.clf()
        self.imagePlt = self.imageFig.add_subplot(111)
        self.image = cv.cvtColor(self.state[self.imageType],cv.COLOR_BGR2RGB)
        self.imagePlt.imshow(cv.cvtColor(self.image,cv.COLOR_BGR2RGB))
        self.imageCanvas.draw()





class HistFrame(tk.Frame):
    def __init__(self, master=None,state=iS.imageState.copy(),imageLabelText = ""):
        super().__init__(master)
        self.master = master
        self.state = state
        self.imageLabelText = imageLabelText
        self.__createHistLabel()
        self.__createHistFigure()
    
    def loadState(self,state):
        self.state = state
        self.__loadHistState()

    def __createHistLabel(self):
        self.graphLabel = tk.Label(self,text=self.imageLabelText)
        self.graphLabel.grid(row=0,column=0)
    def __createHistFigure(self):
        self.histFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        self.histCanvas = FigureCanvasTkAgg(self.histFig,self)
        self.histCanvas.get_tk_widget().grid(row=1,column=0)
        # Toolbar has to go in Frame to back with grid
        histToolbarFrame = tk.Frame(self)
        histToolbarFrame.grid(row=2,column=0)
        histToolbar = NavigationToolbar2Tk(self.histCanvas,histToolbarFrame)

    def __loadHistState(self):
        neighborNumbers = list()
        for cell in self.state[iST.CELLS]:
            neighborNumbers.append(len(cell[ct.NEIGHBORS]))
        self.histFig.clf()
        self.histPlt = self.histFig.add_subplot(111)        
        self.histPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
        self.histCanvas.draw()

