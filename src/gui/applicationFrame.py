########################
##        About       ##
########################
# The root overhead of the gui.
# It also currently holds the state machine and cards.
# Loads state cards to gui panels, and holds old states for later
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import topMenu as tm
from . import graphFrame as gf
from . import optionsFrame as of
import dataTypes.imageState as iS
from dataTypes.dataTypeTraits import imageStateTraits as iST
from app import App


class AppFrame(tk.Frame):
    def __init__(self, master=None, appCore=App()):
        super().__init__(master)
        self.appCore = appCore
        self.__bindEvents()
        #Layout manager
        self.grid()
        #Menu bar
        self.topMenuBar = tm.TopMenu(self)
        self.master.config(menu=self.topMenuBar)
        #Frame for graphs
        self.graphFrame = gf.GraphZoneFrame(self,state=self.appCore.getState())
        self.graphFrame.grid(row=0,column=0)
        #Options
        self.optionsFrame = of.OptionsZoneFrame(self,state=self.appCore.getState())
        self.optionsFrame.grid(row=1,column=0)


    # This is the main event handler     
    def __bindEvents(self):
        self.bind("<<OpenFile>>",self.__openImage)
        #Image State Events
        self.bind("<<AddImageState>>",self.__addImageState)
        self.bind("<<UpImageState>>",self.__upImageState)
        self.bind("<<DownImageState>>",self.__downImageState)
        #This needs a more specific function than all reset analysis
        self.bind("<<SubmitFilterOptions>>",self.__updateFilterOptions)
        #Simular to above
        self.bind("<<SubmitNeighborOptions>>",self.__updateNeighborOptions)


    # Opens image from file and loads to current state
    def __openImage(self,event):
        self.appCore.openImage(self.topMenuBar.openImagePath)
        #TODO:: LOAD TO GRAPH PROPERLY
    # Image State Events
    def __addImageState(self,event):
        self.appCore.addImageState()
        # Updates the status display to show new state option
        self.optionsFrame.update()
        #self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])
    def __upImageState(self,event):
        self.appCore.upImageState()
        self.__loadCurrentStateToAll()
    def __downImageState(self,event):
        self.appCore.downImageState()
        self.__loadCurrentStateToAll()
    # Imaging Events
    def __updateFilterOptions(self,event):
        self.appCore.updateFilterOptions()
        self.graphFrame.updateFilterOptions()
    # Neighbor Analysis Events
    def __updateNeighborOptions(self,event):
        self.appCore.updateNeighborOptions()
        self.graphFrame.updateNeighborOptions()
   

    # This passes the current state to all dependants
    def __loadCurrentStateToAll(self):
        self.graphFrame.loadState(self.appCore.getState())
        self.optionsFrame.loadState(self.appCore.getState())

    def getTotalStatesCount(self):
        return self.appCore.getTotalStatesCount()