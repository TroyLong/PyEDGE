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
from app import AppCore

class AppFrame(tk.Frame):
    def __init__(self, master=None, appCore=None):
        super().__init__(master)
        self.appCore = appCore if appCore != None else AppCore()
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
        self.bind("<<OpenFiles>>",self.__openImages)
        #Time Image State Events
        self.bind("<<AddImageStateTime>>",self.__addImageStateTime)
        self.bind("<<UpImageStateTime>>",self.__upImageStateTime)
        self.bind("<<DownImageStateTime>>",self.__downImageStateTime)
        #Z Image State Events
        self.bind("<<AddImageStateZ>>",self.__addImageStateZ)
        self.bind("<<UpImageStateZ>>",self.__upImageStateZ)
        self.bind("<<DownImageStateZ>>",self.__downImageStateZ)
        #This needs a more specific function than all reset analysis
        self.bind("<<SubmitFilterOptions>>",self.__updateFilterOptions)
        #Simular to above
        self.bind("<<SubmitNeighborOptions>>",self.__updateNeighborOptions)
        self.bind("<<StartMultiStateAnalysis>>",self.__startStateUnionAnalysis)
        self.bind("<<ExportState>>",self.__exportState)
        self.bind("<<ExportSuperState>>",self.__exportSuperState)
    # Opens image from file and loads to current state
    def __openImage(self,event):
        self.appCore.openImage(self.topMenuBar.openImagePath)
        self.__loadCurrentStateToAll()
        #TODO:: LOAD TO GRAPH PROPERLY
    def __openImages(self,event):
        self.appCore.openImages(self.topMenuBar.openImagePaths)
    # Time Image State Events
    def __addImageStateTime(self,event):
        self.appCore.addImageStateTime()
        # Updates the status display to show new state option
        self.optionsFrame.update()
        #self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])
    def __upImageStateTime(self,event):
        self.appCore.upImageStateTime()
        self.__loadCurrentStateToAll()
    def __downImageStateTime(self,event):
        self.appCore.downImageStateTime()
        self.__loadCurrentStateToAll()
     # Z Image State Events
    def __addImageStateZ(self,event):
        self.appCore.addImageStateZ()
        # Updates the status display to show new state option
        self.optionsFrame.update()
        #self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])
    def __upImageStateZ(self,event):
        self.appCore.upImageStateZ()
        self.__loadCurrentStateToAll()
    def __downImageStateZ(self,event):
        self.appCore.downImageStateZ()
        self.__loadCurrentStateToAll()
    # Imaging Events
    def __updateFilterOptions(self,event):
        self.appCore.updateFilterOptions()
        self.graphFrame.updateFilterOptions()
    # Neighbor Analysis Events
    def __updateNeighborOptions(self,event):
        self.appCore.updateNeighborOptions()
        self.graphFrame.updateNeighborOptions()
   # processes multiple images against each other
    def __startStateUnionAnalysis(self,event):
        self.appCore.startStateUnionAnalysis()
        self.graphFrame.loadStateUnion(self.appCore.stateUnion)

    # Export Events
    def __exportState(self,event):
        self.appCore.exportState()
    def __exportSuperState(self,event):
        self.appCore.exportSuperState()

    # This passes the current state to all dependants
    def __loadCurrentStateToAll(self):
        self.graphFrame.loadState(self.appCore.getState())
        self.optionsFrame.loadState(self.appCore.getState())

    def getTotalStatesCount(self):
        return self.appCore.getTotalStatesCount()