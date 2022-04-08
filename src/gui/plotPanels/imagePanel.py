########################
##        About       ##
########################
# These panels holds images of the data
########################
## Imported Libraries ##
########################
# Image Analysis Libraries
import cv2 as cv
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
########################
## Internal Libraries ##
########################
from dataTypes.dataTypeTraits import imageStateTraits as iST
from gui.plotPanels import plotPanel as pP


class ImagePanel(pP.PlotPanel):
    def __init__(self, master=None,state=None,title = "",image_type=None):
        super().__init__(master,state,title)
        self.image_type = image_type
    
    def load(self,state):
        if super().load(state):
            self.__load_image()
    
    def __load_image(self):
        self.figure.clf()
        self.image_plot = self.figure.add_subplot(111)
        # TODO:: replace with match statement after april
        if self.image_type == iST.IMAGE:
            self.image = cv.cvtColor(self.state.image,cv.COLOR_BGR2RGB)
        elif self.image_type == iST.FILTERED_IMAGE:
            self.image = cv.cvtColor(self.state.filtered_image,cv.COLOR_BGR2RGB)
        elif self.image_type == iST.NEIGHBOR_IMAGE:
            self.image = cv.cvtColor(self.state.neighbor_image,cv.COLOR_BGR2RGB)
        self.image_plot.imshow(cv.cvtColor(self.image,cv.COLOR_BGR2RGB))
        axes = self.figure.gca()
        axes.format_coord = lambda x, y: ''
        self.canvas.draw()