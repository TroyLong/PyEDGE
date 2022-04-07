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
    def __init__(self, master=None,state=None,title = "",imageType=None):
        super().__init__(master,state,title)
        self.imageType = imageType
    
    def loadState(self,state):
        if super().loadState(state):
            self.__loadImageState()
    
    def __loadImageState(self):
        self.plotFig.clf()
        self.imagePlt = self.plotFig.add_subplot(111)
        # TODO:: replace with match statement after april
        if self.imageType == iST.IMAGE:
            self.image = cv.cvtColor(self.state.image,cv.COLOR_BGR2RGB)
        elif self.imageType == iST.FILTERED_IMAGE:
            self.image = cv.cvtColor(self.state.filtered_image,cv.COLOR_BGR2RGB)
        elif self.imageType == iST.NEIGHBOR_IMAGE:
            self.image = cv.cvtColor(self.state.neighbor_image,cv.COLOR_BGR2RGB)
        self.imagePlt.imshow(cv.cvtColor(self.image,cv.COLOR_BGR2RGB))
        axes = self.plotFig.gca()
        axes.format_coord = lambda x, y: ''
        self.plotCanvas.draw()