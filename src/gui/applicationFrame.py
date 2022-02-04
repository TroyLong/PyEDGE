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


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__initImageState()
        self.__bindEvents()
        #Layout manager
        self.grid()
        #Menu bar
        self.topMenuBar = tm.TopMenu(self)
        self.master.config(menu=self.topMenuBar)
        #Frame for graphs
        self.graphFrame = gf.GraphZoneFrame(self,state=self.imageStateList[self.imageStateIndex])
        self.graphFrame.grid(row=0,column=0)
        #Options
        self.optionsFrame = of.OptionsZoneFrame(self,state=self.imageStateList[self.imageStateIndex])
        self.optionsFrame.grid(row=1,column=0)
    # There is a list of states, each of which can be loaded and passed to the whole program
    def __initImageState(self):
        self.imageStateIndex = 0
        self.imageStateList = [iS.imageState.copy()]
        self.statusMessage = ""


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
        #Cell Focus Panel Events
        self.bind("<<PreviousCell>>",self.__previousCell)
        self.bind("<<NextCell>>",self.__nextCell)

    # Opens image from file and loads to current state
    def __openImage(self,event):
        self.graphFrame.openFile(self.topMenuBar.openImagePath)
    # Image State Events
    def __addImageState(self,event):
        self.imageStateList.append(iS.imageState.copy())
        # Updates the status display to show new state option
        self.optionsFrame.update()
        #self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])
    def __upImageState(self,event):
        self.imageStateIndex += 1 if (self.imageStateIndex<len(self.imageStateList)-1) else 0
        self.__loadCurrentStateToAll()
    def __downImageState(self,event):
        self.imageStateIndex -= 1 if (self.imageStateIndex>0) else 0
        self.__loadCurrentStateToAll()
    # Imaging Events
    def __updateFilterOptions(self,event):
        iS.printState(self.imageStateList[self.imageStateIndex])
        self.graphFrame.updateFilterOptions()
    # Neighbor Analysis Events
    def __updateNeighborOptions(self,event):
        iS.printState(self.imageStateList[self.imageStateIndex])
        self.graphFrame.updateNeighborOptions()
    def __previousCell(self,event):
        pass
    def __nextCell(self,event):
        pass
    # This passes the current state to all dependants
    def __loadCurrentStateToAll(self):
        self.graphFrame.loadState(self.imageStateList[self.imageStateIndex])
        self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])

    # This passes information about the number of states, and which is active now
    def getTotalStatesCount(self):
        return (self.imageStateIndex,len(self.imageStateList))

    def getStatusMessage(self):
        return self.statusMessage