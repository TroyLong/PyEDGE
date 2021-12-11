########################
##        About       ##
########################
# These panels hold visual data such as images or graphs.
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
# Neighbor Libraries
# State Machine Libraries
import imageState as iS
from imageState import imageStateTraits as iST


# PlotPanel parent class for inheritance. Creates figures
class PlotPanel(iS.StateMachinePanel):
    def __init__(self, master=None,state=iS.imageState.copy(),title = ""):
        super().__init__(master,state)
        self.title = title
        self.__createPlotTitle()
        self.__createPlotFigure()
    
    def __createPlotTitle(self):
        self.plotTitle = tk.Label(self,text=self.title)
        self.plotTitle.grid(row=0,column=0)
    
    def __createPlotFigure(self):
        self.plotFig = plt.Figure(figsize=(4,4), dpi=100, tight_layout=True)
        # Canvas for the image or graph to display to
        self.plotCanvas = FigureCanvasTkAgg(self.plotFig,self)
        self.plotCanvas.get_tk_widget().grid(row=1,column=0)
        # Toolbar has to go in Frame to back with grid
        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=2,column=0)
        imageToolbar = NavigationToolbar2Tk(self.plotCanvas,toolbarFrame)
    
    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def loadBlankImage(self):
        self.plotFig.clf()
        self.plotCanvas.draw()




class ImagePanel(PlotPanel):
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




class HistPanel(PlotPanel):
    def __init__(self, master=None,state=iS.imageState.copy(),title = ""):
        super().__init__(master,state,title)
    
    def loadState(self,state):
        if super().loadState(state):
            self.__loadHistState()

    def __loadHistState(self):
        neighborNumbers = list()
        # Only draw histogram if there are cells to create it with
        if len(self.state[iST.CELLS]):
            for cell in self.state[iST.CELLS]:
                neighborNumbers.append(len(cell[ct.NEIGHBORS]))
            self.plotFig.clf()
            self.histPlt = self.plotFig.add_subplot(111)        
            self.histPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
            self.plotCanvas.draw()