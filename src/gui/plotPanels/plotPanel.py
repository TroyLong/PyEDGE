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
import gui.stateMachineFrame as sMF

# PlotPanel parent class for inheritance. Creates figures
class PlotPanel(sMF.StateMachineFrame):
    def __init__(self, master=None,state=None,title = ""):
        super().__init__(master,state)
        self.title = title
        self.__createPlotTitle()
        self.__createPlotFigure()
    
    def __createPlotTitle(self):
        self.plotTitle = tk.Label(self,text=self.title)
        self.plotTitle.grid(row=0,column=0)
    
    def __createPlotFigure(self):
        self.plotFig = plt.Figure(figsize=(3.75,4), dpi=100, tight_layout=True)
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