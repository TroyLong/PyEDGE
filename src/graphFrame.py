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
########################
## Internal Libraries ##
########################
# Plot Panel Libraries
from plotPanel import ImagePanel, HistPanel
# Image Analysis Libraries
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
        self.originalImageFrame = ImagePanel(self,state=self.state,title="Original",imageType=iST.IMAGE)
        self.originalImageFrame.grid(row=1,column=column)
    def __createFilteredGraph(self,column):
        self.filteredImageFrame = ImagePanel(self,state=self.state,title="Filtered",imageType=iST.FILTERED_IMAGE)
        self.filteredImageFrame.grid(row=1,column=column)
    def __createNeighborGraph(self,column):
        self.neighborImageFrame = ImagePanel(self,state=self.state,title="Neighbor Mapping",imageType=iST.NEIGHBOR_IMAGE)
        self.neighborImageFrame.grid(row=1,column=column)
    def __createNeighborHistogramGraph(self,column):
        self.neighborHistFrame = HistPanel(self,state=self.state,title="Neighbor Histogram")
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