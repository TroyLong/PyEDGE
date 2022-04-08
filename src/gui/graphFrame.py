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
    def __init__(self, master=None,state=None,kernel_state=None):
        super().__init__(master)
        self.master = master
        self.state = state if state != None else State()
        self.kernel_state = kernel_state if kernel_state != None else State()
        self.__create_graphs()

    def load(self,state):
        if super().load(state):
            self.__load_images()
        else:
            self.__load_blank_images()

    def load_kernel_state(self,kernel_state):
        self.kernel_state=kernel_state
        self.__load_images()

    def open_file(self,imagePath):
        self.__load_images()

    # These functions can be called to have images re-created
    def update_filter(self):
        if self.state.image_opened:
            #self.__createFilteredImageAndCells()
            self.update_neighbor_filter()
    def update_neighbor_filter(self):
        if self.state.image_opened:
            #self.__createNeighborImage()
            # TODO:: Do I still use these functions?
            # Yes, but why?
            self.__load_images()


    # These functions create the spaces where the images can be placed
    def __create_graphs(self):
        self.grid()
        self.__create_original(0)
        self.__create_filtered(1)
        self.__create_neighbor(2)
        self.__create_neighbor_histogram(3)
        self.__create_kernel(4)

    def __create_original(self,column):
        self.original = ImagePanel(self,state=self.state,title="Original",image_type=iST.IMAGE)
        self.original.grid(row=1,column=column)
    def __create_filtered(self,column):
        self.filtered = ImagePanel(self,state=self.state,title="Filtered",image_type=iST.FILTERED_IMAGE)
        self.filtered.grid(row=1,column=column)
    def __create_neighbor(self,column):
        self.neighbor = ImagePanel(self,state=self.state,title="Neighbor Mapping",image_type=iST.NEIGHBOR_IMAGE)
        self.neighbor.grid(row=1,column=column)
    def __create_neighbor_histogram(self,column):
        self.neighbor_hist = HistPanel(self,state=self.state,title="Neighbor Histogram")
        self.neighbor_hist.grid(row=1,column=column)
    def __create_kernel(self,column):
        self.kernel = ImagePanel(self,state=self.kernel_state,title="Multi-State Analysis",image_type=iST.NEIGHBOR_IMAGE)
        self.kernel.grid(row=1,column=column)


    # These functions load pre-created images to the graphs
    def __load_images(self):
        self.original.load(self.state)
        self.filtered.load(self.state)
        self.neighbor.load(self.state)
        self.neighbor_hist.load(self.state)
        self.kernel.load(self.kernel_state)

    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def __load_blank_images(self):
        self.original.load_blank_image()
        self.filtered.load_blank_image()
        self.neighbor.load_blank_image()
        self.neighbor_hist.load_blank_image()
        self.kernel.load_blank_image()