########################
##        About       ##
########################
# This panel alter neighbor finding parameters
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP


# Controls neighbor finding constraints
class NeighborOptionsPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Neighbor Options")
        self._createDeviationOption(2)
        self._createMaxNeighborDistanceOption(3)
        self._createUpperCutoffDistanceOption(4)
        self._createNeighborOptionsSubmitButton(5)
        self._createNeighborOptionsSubmitAllButton(6)

    # Called to load new state
    def loadState(self,state):
        if super().loadState(state):
            self._loadDeviationOptionState()
            self._loadMaxNeighborDistanceOptionState()
            self._loadUpperCutoffDistanceOptionState()
            
    # These functions are only called for creation
    def _createDeviationOption(self,row):
        optionLabel = tk.Label(self,text="Neighbor Distance Deviation:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.deviationEntry = tk.Entry(self)
        self.deviationEntry.insert(0,"15.0")
        self.deviationEntry.grid(row=row,column=1)
    def _createMaxNeighborDistanceOption(self,row):
        optionLabel = tk.Label(self,text="Maximum Distance to Neighbors:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.maxNeighborDistanceEntry = tk.Entry(self)
        self.maxNeighborDistanceEntry.insert(0,"80000.0")
        self.maxNeighborDistanceEntry.grid(row=row,column=1)
    def _createUpperCutoffDistanceOption(self,row):
        optionLabel = tk.Label(self,text="Tree sorting cutoff distance:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.upperCutoffDistanceEntry = tk.Entry(self)
        self.upperCutoffDistanceEntry.insert(0,"5000.0")
        self.upperCutoffDistanceEntry.grid(row=row,column=1)
    def _createNeighborOptionsSubmitButton(self,row):
        optionsSubmitButton = tk.Button(self,text="Submit",command=self.__optionsSubmit)
        optionsSubmitButton.grid(row=row,column=0,columnspan=2)
    def _createNeighborOptionsSubmitAllButton(self,row):
        optionsSubmitAllButton = tk.Button(self,text="Submit All",command=self.__optionsSubmitAll)
        optionsSubmitAllButton.grid(row=row,column=0,columnspan=2)

    # These functions are called each time a state is loaded
    def _loadDeviationOptionState(self):
        self.deviationEntry.delete(0,tk.END)
        self.deviationEntry.insert(0,self.state.deviation)
    def _loadMaxNeighborDistanceOptionState(self):
        self.maxNeighborDistanceEntry.delete(0,tk.END)
        self.maxNeighborDistanceEntry.insert(0,self.state.max_neighbor_dist)
    def _loadUpperCutoffDistanceOptionState(self):
        self.upperCutoffDistanceEntry.delete(0,tk.END)
        self.upperCutoffDistanceEntry.insert(0,self.state.upper_cutoff_dist)

    # Saves option data to loaded state before button event activates
    def __optionsSubmit(self):
        self.saveState()
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def __optionsSubmitAll(self):
        self.saveState()
        self.master.event_generate("<<SubmitAllNeighborOptions>>")
    def saveState(self):
        if super().saveState():
            self.state.deviation = self._getFloatEntry(self.state.deviation,self.deviationEntry)
            self.state.max_neighbor_dist = self._getFloatEntry(self.state.max_neighbor_dist,self.maxNeighborDistanceEntry)
            self.state.upper_cutoff_dist = self._getFloatEntry(self.state.upper_cutoff_dist,self.upperCutoffDistanceEntry)