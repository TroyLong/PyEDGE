# TODO:: The neighbor analysis is continually adding guessed neighbors each time it is run
########################
##        About       ##
########################
# This displays cell images, the filtered image, and the neighbor mappings
# It may also display graphical aids to analyse the date
########################
## Internal Libraries ##
########################
import analysis.segmentImage as sI
import analysis.neighborAnalysis as nA
import analysis.filters.cellFilters.cellFilters as cF
from dataTypes.state import State
import gui.stateMachineFrame as sMF
from dataTypes.dataTypeTraits import imageStateTraits as iST
from gui.plotPanels.imagePanel import ImagePanel
from gui.plotPanels.histPanel import HistPanel


class GraphZoneFrame(sMF.StateMachineFrame):
    def __init__(self, master=None,state=None,stateUnion=None):
        super().__init__(master)
        self.master = master
        self.state = state if state != None else State()
        self.stateUnion = stateUnion if stateUnion != None else State()
        self.__createGraphs()

    def loadState(self,state):
        if super().loadState(state):
            self.__loadImages()
        else:
            self.__loadBlankImages()

    # TODO:: Bad Form
    def loadStateUnion(self,stateUnion):
        self.stateUnion=stateUnion
        self.__loadImages()

    def openFile(self,imagePath):
        self.__loadImages()

    # These functions can be called to have images re-created
    def updateFilterOptions(self):
        if self.state.image_opened:
            #self.__createFilteredImageAndCells()
            self.updateNeighborOptions()
    def updateNeighborOptions(self):
        if self.state.image_opened:
            #self.__createNeighborImage()
            # TODO:: Do I still use these functions?
            # Yes, but why?
            self.__loadImages()


    # These functions create the spaces where the images can be placed
    def __createGraphs(self):
        self.grid()
        self.__createOriginalGraph(0)
        self.__createFilteredGraph(1)
        self.__createNeighborGraph(2)
        self.__createNeighborHistogramGraph(3)
        self.__createStateUnionAnalysisGraph(4)

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
    def __createStateUnionAnalysisGraph(self,column):
        self.stateUnionFrame = ImagePanel(self,state=self.stateUnion,title="Multi-State Analysis",imageType=iST.NEIGHBOR_IMAGE)
        self.stateUnionFrame.grid(row=1,column=column)


    # These functions load pre-created images to the graphs
    def __loadImages(self):
        self.originalImageFrame.loadState(self.state)
        self.filteredImageFrame.loadState(self.state)
        self.neighborImageFrame.loadState(self.state)
        self.neighborHistFrame.loadState(self.state)
        self.stateUnionFrame.loadState(self.stateUnion)

    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def __loadBlankImages(self):
        self.originalImageFrame.loadBlankImage()
        self.filteredImageFrame.loadBlankImage()
        self.neighborImageFrame.loadBlankImage()
        self.neighborHistFrame.loadBlankImage()
        self.stateUnionFrame.loadBlankImage()