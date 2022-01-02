########################
##        About       ##
########################
# This panel manipulates image filtering
########################
## Imported Libraries ##
########################
import tkinter as tk
import dataTypes.imageState as iS
########################
## Internal Libraries ##
########################
from dataTypes.imageStateTraits import imageStateTraits as iST
from . import controlPanel as cP

# Controls image filter options
class FilterOptionsPanel(cP.ControlPanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master,state,"Filter Options")
        self._createFilterDiameterOption(2)
        self._createSigmaColorOption(3)
        self._createSigmaSpaceOption(4)
        self._createAdaptiveBlockSizeOption(5)
        self._createFilterOptionsSubmit(6)

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
    
    # These functions are called each time a state is loaded
    def _loadFilterDiameterOptionState(self):
        self.filterDiameterEntry.delete(0,tk.END)
        self.filterDiameterEntry.insert(0,self.state[iST.FILTER_DIAMETER])
    def _loadSigmaColorOptionState(self):
        self.sigmaColorEntry.delete(0,tk.END)
        self.sigmaColorEntry.insert(0,self.state[iST.SIGMA_COLOR])
    def _loadSigmaSpaceOptionState(self):
        self.sigmaSpaceEntry.delete(0,tk.END)
        self.sigmaSpaceEntry.insert(0,self.state[iST.SIGMA_SPACE])
    def _loadAdaptiveBlockSizeOptionState(self):
        self.adaptiveBlockSizeEntry.delete(0,tk.END)
        self.adaptiveBlockSizeEntry.insert(0,self.state[iST.ADAPTIVE_BLOCKSIZE])

    # Saves option data to loaded state before button event activates
    def __optionsSubmit(self):
        self.saveState()
        self.master.event_generate("<<SubmitFilterOptions>>")
    def saveState(self):
        if super().saveState():
            self.state[iST.FILTER_DIAMETER] = self._getIntEntry(self.state[iST.FILTER_DIAMETER],self.filterDiameterEntry)
            self.state[iST.SIGMA_COLOR] = self._getFloatEntry(self.state[iST.SIGMA_COLOR],self.sigmaColorEntry)
            self.state[iST.SIGMA_SPACE] = self._getFloatEntry(self.state[iST.SIGMA_SPACE],self.sigmaSpaceEntry)
            self.state[iST.ADAPTIVE_BLOCKSIZE] = self._getIntEntry(self.state[iST.ADAPTIVE_BLOCKSIZE],self.adaptiveBlockSizeEntry)