########################
##        About       ##
########################
# These panels hold visual data such as images or graphs.
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
from dataTypes.dataTypeTraits import cellTraits as cT
from dataTypes.dataTypeTraits import imageStateTraits as iST
from gui.plotPanels import plotPanel as pP


class HistPanel(pP.PlotPanel):
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
                neighborNumbers.append(len(cell[cT.NEIGHBORS]))
            self.plotFig.clf()
            self.histPlt = self.plotFig.add_subplot(111)        
            self.histPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
            self.plotCanvas.draw()