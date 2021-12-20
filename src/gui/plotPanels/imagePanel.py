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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
########################
## Internal Libraries ##
########################
import dataTypes.imageState as iS
from gui.plotPanels import plotPanel as pP

class ImagePanel(pP.PlotPanel):
    def __init__(self, master=None,state=iS.imageState.copy(),title = "",imageType=None):
        super().__init__(master,state,title)
        self.imageType = imageType
    
    def loadState(self,state):
        if super().loadState(state):
            self.__loadImageState()
    
    def __loadImageState(self):
        self.plotFig.clf()
        self.imagePlt = self.plotFig.add_subplot(111)
        self.image = cv.cvtColor(self.state[self.imageType],cv.COLOR_BGR2RGB)
        self.imagePlt.imshow(cv.cvtColor(self.image,cv.COLOR_BGR2RGB))
        self.plotCanvas.draw()