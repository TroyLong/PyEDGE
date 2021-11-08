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
        self.graphFrame = gf.GraphFrame(self,self.deviation,self.maxNeighborDistance,self.upperCutoffDistance)
        self.graphFrame.grid(row=0,column=0)
        #Options
        self.optionsFrame = of.OptionsFrame(self)
        self.optionsFrame.grid(row=1,column=0)


    def __initImageState(self):
        self.imageStateIndex = 0
        self.imageStateList = list(None)

        
    ##TODO:: I NEED to work on more event functions, so each setting submition gets its own function.
    def __bindEvents(self):
        self.bind("<<OpenFile>>",self.__openImage)
        #This needs a more specific function than all reset analysis
        self.bind("<<SubmitFilterOptions>>",self.__updateFilterOptions)
        #Simular to above
        self.bind("<<SubmitNeighborOptions>>",self.__updateNeighborOptions)
    def __openImage(self,event):
        self.graphFrame.openImage(self.topMenuBar.openImagePath)
        self.imageStateList.append(self.__getImageState())
    def __updateFilterOptions(self,event):
        self.graphFrame.updateFilterOptions(self.optionsFrame.filterOptions.getOptions())
    def __updateNeighborOptions(self,event):
        self.graphFrame.updateNeighborOptions(self.optionsFrame.neighborOptions.getOptions())
    
    #TODO:: I'm right here. Trying to implement a state loader for different images
    def __getImageState(self):
        images = self.graphFrame.getImageStateInfo()
        options = self.optionsFrame.getImageStateInfo()
        imageState = iS.imageState.copy()
        imageState[iST.IMAGE] = images[0]
        imageState[iST.FILTERED_IMAGE] = images[1]
        imageState[iST.NEIGHBOR_IMAGE] = images[2]
        imageState[iST.DEVIATION] = options[0]
        imageState[iST.MAX_NEIGHBHOR_DIST] = options[1]
        imageState[iST.UPPER_CUTOFF_DIST] = options[2]
        self.imageStateList.append(imageState)
        self.imageStateIndex += 1





# This actually starts the code
app = App()
app.master.title("PyEDGE")
app.mainloop()