########################
##        About       ##
########################
# This panel manipulates image filtering
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP

# Controls image filter options
class FilterOptionsPanel(cP.ControlPanel):
    def __init__(self, master=None, state=None):
        super().__init__(master,state,"Filter Options")
        self._createFilterDiameterOption(2)
        self._createSigmaColorOption(3)
        self._createSigmaSpaceOption(4)
        self._createAdaptiveBlockSizeOption(5)
        self._createFilterOptionsSubmit(6)
        self._createFilterOptionsSubmitAll(7)

    # Called to load new state
    def loadState(self,state):
        if super().loadState(state):
            self._loadFilterDiameterOptionState()
            self._loadSigmaColorOptionState()
            self._loadSigmaSpaceOptionState()
            self._loadAdaptiveBlockSizeOptionState()

    # These functions are only called for creation
    def _createFilterDiameterOption(self,row):
        optionLabel = tk.Label(self,text="Filter Diameter:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.filterDiameterEntry = tk.Entry(self)
        self.filterDiameterEntry.insert(0,"10")
        self.filterDiameterEntry.grid(row=row,column=1)
    def _createSigmaColorOption(self,row):
        optionLabel = tk.Label(self,text="Bilinear Filter Sigma Color:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.sigmaColorEntry = tk.Entry(self)
        self.sigmaColorEntry.insert(0,"75")
        self.sigmaColorEntry.grid(row=row,column=1)
    def _createSigmaSpaceOption(self,row):
        optionLabel = tk.Label(self,text="Bilinear Filter Sigma Space:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.sigmaSpaceEntry = tk.Entry(self)
        self.sigmaSpaceEntry.insert(0,"75")
        self.sigmaSpaceEntry.grid(row=row,column=1)
    def _createAdaptiveBlockSizeOption(self,row):
        optionLabel = tk.Label(self,text="Adaptive Threshold Block Size:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.adaptiveBlockSizeEntry = tk.Entry(self)
        self.adaptiveBlockSizeEntry.insert(0,"151")
        self.adaptiveBlockSizeEntry.grid(row=row,column=1)
    def _createFilterOptionsSubmit(self,row):
        self.filterOptionsSubmitButton = tk.Button(self,text="Submit",command=self.__optionsSubmit)
        self.filterOptionsSubmitButton.grid(row=row,column=0,columnspan=2)
    def _createFilterOptionsSubmitAll(self,row):
        self.filterOptionsSubmitAllButton = tk.Button(self,text="Submit All",command=self.__optionsSubmitAll)
        self.filterOptionsSubmitAllButton.grid(row=row,column=0,columnspan=2)
    
    # These functions are called each time a state is loaded
    def _loadFilterDiameterOptionState(self):
        self.filterDiameterEntry.delete(0,tk.END)
        self.filterDiameterEntry.insert(0,self.state.filter_diameter)
    def _loadSigmaColorOptionState(self):
        self.sigmaColorEntry.delete(0,tk.END)
        self.sigmaColorEntry.insert(0,self.state.sigma_color)
    def _loadSigmaSpaceOptionState(self):
        self.sigmaSpaceEntry.delete(0,tk.END)
        self.sigmaSpaceEntry.insert(0,self.state.sigma_space)
    def _loadAdaptiveBlockSizeOptionState(self):
        self.adaptiveBlockSizeEntry.delete(0,tk.END)
        self.adaptiveBlockSizeEntry.insert(0,self.state.adaptive_blocksize)

    # Saves option data to loaded state before button event activates
    def __optionsSubmit(self):
        self.saveState()
        self.master.event_generate("<<SubmitFilterOptions>>")
    def __optionsSubmitAll(self):
        self.saveState()
        self.master.event_generate("<<SubmitAllFilterOptions>>")
    def saveState(self):
        if super().saveState():
            self.state.filter_diameter = self._getIntEntry(self.state.filter_diameter,self.filterDiameterEntry)
            self.state.sigma_color = self._getFloatEntry(self.state.sigma_color,self.sigmaColorEntry)
            self.state.sigma_space = self._getFloatEntry(self.state.sigma_space,self.sigmaSpaceEntry)
            self.state.adaptive_blocksize = self._getIntEntry(self.state.adaptive_blocksize,self.adaptiveBlockSizeEntry)