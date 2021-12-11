# TODO:: The neighbor analysis is continually adding guessed neighbors each time it is run
########################
##        About       ##
########################
# This displays cell images, the filtered image, and the neighbor mappings
# It may also display graphical aids to analyse the date
########################
## Imported Libraries ##
########################
# Image Analysis Libraries
import cv2 as cv
# Gui Libraries
import tkinter as tk
# Graphing Libraries
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
########################
## Internal Libraries ##
########################
# Image Analysis Libraries
from cell import cellTraits as ct
import segmentImage as sI
# Neighbor Libraries
import neighborAnalysis as nA
# State Machine Libraries
import imageState as iS
from imageState import imageStateTraits as iST


class GraphZoneFrame(iS.StateMachinePanel):
    def __init__(self, master=None,state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
        self.__createGraphs()

    def loadState(self,state):
        if super().loadState(state):
            self.__loadImages()
        else:
            self.__loadBlankImages()

    def openFile(self,imagePath):
        self.state[iST.IMAGE_OPENED] = True
        self.imagePath = imagePath
        self.__createOriginalImage()
        self.__createFilteredImageAndCells()
        self.__createNeighborImage()
        self.__loadImages()

    # These functions can be called to have images re-created
    def updateFilterOptions(self):
        if self.state[iST.IMAGE_OPENED]:
            self.__createFilteredImageAndCells()
            self.updateNeighborOptions()
    def updateNeighborOptions(self):
        if self.state[iST.IMAGE_OPENED]:
            self.__createNeighborImage()
            #TODO:: Do I still use these functions?
            self.__loadImages()

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
        # TODO:: If Adaptive Blocksize is > 2 or %2 = 1 this works. Otherwise I get an error
        self.state[iST.CELLS],self.state[iST.FILTERED_IMAGE] = sI.segmentImage(image=self.state[iST.IMAGE],
                                                                                diameter=self.state[iST.FILTER_DIAMETER],
                                                                                bfSigmaColor=self.state[iST.SIGMA_COLOR],
                                                                                bfSigmaSpace=self.state[iST.SIGMA_SPACE],
                                                                                atBlockSize=self.state[iST.ADAPTIVE_BLOCKSIZE])
    def __createNeighborImage(self):
        self.state[iST.NEIGHBOR_IMAGE] = self.state[iST.FILTERED_IMAGE].copy()    
        nA.processNeighorAnalysis(self.state)

    # These functions load pre-created images to the graphs
    def __loadImages(self):
        self.originalImageFrame.loadState(self.state)
        self.filteredImageFrame.loadState(self.state)
        self.neighborImageFrame.loadState(self.state)
        self.neighborHistFrame.loadState(self.state)

    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def __loadBlankImages(self):
        self.originalImageFrame.loadBlankImage()
        self.filteredImageFrame.loadBlankImage()
        self.neighborImageFrame.loadBlankImage()
        self.neighborHistFrame.loadBlankImage()
        




class ImageFrame(iS.StateMachinePanel):
    def __init__(self, master=None,state=iS.imageState.copy(),imageType=None,imageLabelText = ""):
        super().__init__(master,state)
        self.imageLabelText = imageLabelText
        self.imageType = imageType
        self.__createImageLabel()
        self.__createImageFigure()
    
    def loadState(self,state):
        if super().loadState(state):
            self.__loadImageState()

    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def loadBlankImage(self):
        self.imageFig.clf()
        self.imageCanvas.draw()

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





class HistFrame(iS.StateMachinePanel):
    def __init__(self, master=None,state=iS.imageState.copy(),imageLabelText = ""):
        super().__init__(master,state)
        self.imageLabelText = imageLabelText
        self.__createHistLabel()
        self.__createHistFigure()
    
    def loadState(self,state):
        if super().loadState(state):
            self.__loadHistState()

    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def loadBlankImage(self):
        self.histFig.clf()
        self.histCanvas.draw()

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
        # Only draw histogram if there are cells to create it with
        if len(self.state[iST.CELLS]):
            for cell in self.state[iST.CELLS]:
                neighborNumbers.append(len(cell[ct.NEIGHBORS]))
            self.histFig.clf()
            self.histPlt = self.histFig.add_subplot(111)        
            self.histPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
            self.histCanvas.draw()

