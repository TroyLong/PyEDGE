from dataTypes.state import State
from dataTypes.dataTypeTraits import imageStateTraits as iST
from gui.plotPanels.imagePanel import ImagePanel
from gui.plotPanels.histPanel import HistPanel
from ..graphFrame import GraphZoneFrame

class GraphZoneFrame(GraphZoneFrame):
    def __init__(self, master=None,state=None,kernel_state=None):
        self.kernel_state = kernel_state if kernel_state != None else State()
        super().__init__(master,state)

    def load_kernel_state(self,kernel_state):
        self.kernel_state=kernel_state
        self.load_images()

    # These functions can be called to have images re-created
    def update_filter(self):
        if self.state.image_opened:
            self.update_neighbor_filter()
    def update_neighbor_filter(self):
        if self.state.image_opened:
            self.load_images()

    def create_graphs(self):
        self._create_original(0)
        self._create_filtered(1)
        self._create_neighbor(2)
        self._create_neighbor_histogram(3)
        self._create_kernel(4)
    def _create_original(self,column):
        self.original = ImagePanel(self,state=self.state,title="Original",image_type=iST.IMAGE)
        self.original.grid(row=1,column=column)
    def _create_filtered(self,column):
        self.filtered = ImagePanel(self,state=self.state,title="Filtered",image_type=iST.FILTERED_IMAGE)
        self.filtered.grid(row=1,column=column)
    def _create_neighbor(self,column):
        self.neighbor = ImagePanel(self,state=self.state,title="Neighbor Mapping",image_type=iST.NEIGHBOR_IMAGE)
        self.neighbor.grid(row=1,column=column)
    def _create_neighbor_histogram(self,column):
        self.neighbor_hist = HistPanel(self,state=self.state,title="Neighbor Histogram")
        self.neighbor_hist.grid(row=1,column=column)
    def _create_kernel(self,column):
        self.kernel = ImagePanel(self,state=self.kernel_state,title="Multi-State Analysis",image_type=iST.NEIGHBOR_IMAGE)
        self.kernel.grid(row=1,column=column)

    def load_images(self):
        self.original.load(self.state)
        self.filtered.load(self.state)
        self.neighbor.load(self.state)
        self.neighbor_hist.load(self.state)
        self.kernel.load(self.kernel_state)

    def load_blank_images(self):
        self.original.load_blank_image()
        self.filtered.load_blank_image()
        self.neighbor.load_blank_image()
        self.neighbor_hist.load_blank_image()
        self.kernel.load_blank_image()