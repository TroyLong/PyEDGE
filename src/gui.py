#TODO:: The state machine is sloppy. Currently builds, then sets state, then changes build to new state. Should start with state loaded, then populate first state.
####### IE it is too ad-hoc. This should be fixed by passing the state to the graph and option frames on creation. This will force them to integrate them better.
####### Tighter integration should allow the state to be changed without having as many high level event calls.
#TODO:: Finish implementing the controls with the setting changes.
#TODO:: Add locks to stop buttons from working with invalid input and no images

import tkinter as tk
import topMenu as tm
import graphFrame as gf
import optionsFrame as of
import imageState as iS
from imageState import imageStateTraits as iST


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
        self.graphFrame = gf.GraphFrame(self)
        self.graphFrame.grid(row=0,column=0)
        #Options
        self.optionsFrame = of.OptionsFrame(self)
        self.optionsFrame.grid(row=1,column=0)
    def __initImageState(self):
        self.imageStateIndex = 0
        self.imageStateList = list()

        
    ##TODO:: I NEED to work on more event functions, so each setting submition gets its own function.
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

    def __openImage(self,event):
        self.graphFrame.openImage(self.topMenuBar.openImagePath)
        self.__getImageState()
    # Image State Events
    def __addImageState(self,event):
        self.imageStateList.append(None)
        print(len(self.imageStateList))
    def __upImageState(self,event):
        self.imageStateIndex += 1 if (self.imageStateIndex<len(self.imageStateList)-1) else 0
        print(self.imageStateIndex)
    def __downImageState(self,event):
        self.imageStateIndex -= 1 if (self.imageStateIndex>0) else 0
        print(self.imageStateIndex)
    # Imaging Events
    def __updateFilterOptions(self,event):
        self.graphFrame.updateFilterOptions(self.optionsFrame.filterOptions.getStateInfo())
        self.__getImageState()
    # Neighbor Analysis Events
    def __updateNeighborOptions(self,event):
        self.graphFrame.updateNeighborOptions(self.optionsFrame.neighborOptions.getStateInfo())
        self.__getImageState()

    def __getImageState(self):
        images = self.graphFrame.getStateInfo()
        options = self.optionsFrame.getStateInfo()
        imageState = iS.imageState.copy()
        imageState[iST.IMAGE] = images[0]
        imageState[iST.FILTERED_IMAGE] = images[1]
        imageState[iST.NEIGHBOR_IMAGE] = images[2]
        imageState[iST.DEVIATION] = options[0]
        imageState[iST.MAX_NEIGHBHOR_DIST] = options[1]
        imageState[iST.UPPER_CUTOFF_DIST] = options[2]
        self.imageStateList[self.imageStateIndex] = imageState

    def getStateIndexInfo(self):
        return (self.imageStateIndex,len(self.imageStateList))




# This actually starts the code
app = App()
app.master.title("PyEDGE")
app.mainloop()