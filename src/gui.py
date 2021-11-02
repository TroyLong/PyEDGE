#TODO:: Finish implementing the controls with the setting changes.
#TODO:: Add locks to stop buttons from working with invalid input and no images

import tkinter as tk
import topMenu as tm
import graphFrame as gf
import optionsFrame as of


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.__initApproxConstants()
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


    def __initApproxConstants(self):
        #How far can a center be away from the last center and be in the same set
        self.deviation = 15
        #Sets a longest possible neighbor distance. Really important variable
        self.maxNeighborDistance = 80000
        #Allows a first order approximation to speed up tree branching. Small numbers don't look far enough, large numbers take a long time
        self.upperCutoffDistance = 5000

        
    ##TODO:: I NEED to work on more event functions, so each setting submition gets its own function.
    def __bindEvents(self):
        self.bind("<<OpenFile>>",self.__openImage)
        #This needs a more specific function than all reset analysis
        self.bind("<<SubmitFilterOptions>>",self.__updateFilterOptions)
        #Simular to above
        self.bind("<<SubmitNeighborOptions>>",self.__updateNeighborOptions)
    def __openImage(self,event):
        self.imagePath = self.topMenuBar.openImagePath
        self.graphFrame.openImage(self.imagePath)
    def __updateFilterOptions(self,event):
        self.graphFrame.updateFilterOptions(self.optionsFrame.filterOptions.getOptions())
    def __updateNeighborOptions(self,event):
        self.graphFrame.updateNeighborOptions(self.optionsFrame.neighborOptions.getOptions())






# This actually starts the code
app = App()
app.master.title("PyEDGE")
app.mainloop()