# This frame holds settings for the image processing, and neighbor guessing.
# The file currently includes three classes for convienence, but they could be split if need be
import tkinter as tk
import imageState as iS
from imageState import imageStateTraits as iST


# ControlPanel parent class for inheritance
class ControlPanel(iS.StateMachinePanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master,state)

    def _createTitleBanner(self,text="",fontSize=10,row=1,column=0,columnspan=2):
        bannerLabel = tk.Label(self,text=text)
        bannerLabel.config(font=("Ubuntu",fontSize))
        bannerLabel.grid(row=row,column=column,columnspan=columnspan)
    def _createStatusBanner(self,text="",row=2,column=0,columnspan=2):
        self.statusLabel = tk.Label(self,text=text)
        self.statusLabel.grid(row=row,column=0,columnspan=2)




# This is the main Panel Window Section
class OptionsZoneFrame(ControlPanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
        self.__bindEvents()
        self.grid()
        self._createTitleBanner("Options",fontSize=12,row=0)
        self._createStatePanel(0)
        self._createFilterOptionsPanel(1)
        self._createNeighborOptionsPanel(2)
        self._createCellFocusPanel(3)

# These functions are only called for creation
    def _createStatePanel(self,column):
        self.stateOptions = ImageStatePanel(self,state=self.state)
        self.stateOptions.grid(row=1,column=column,padx=5)
    def _createFilterOptionsPanel(self,column):
        self.filterOptions = FilterOptionsPanel(self,state=self.state)
        self.filterOptions.grid(row=1,column=column,padx=5)
    def _createNeighborOptionsPanel(self,column):
        self.neighborOptions = NeighborOptionsPanel(self,state=self.state)
        self.neighborOptions.grid(row=1,column=column,padx=5)
    def _createCellFocusPanel(self,column):
        self.cellFocusPanel = CellFocusPanel(self, state=self.state)
        self.cellFocusPanel.grid(row=1,column=column,padx=5)

    # Called to load new state
    def loadState(self,state):
        # This insures default settings are saved to previous State if state is changed
        # This does NOT submit the changes for view
        if self.saveState():
            self.filterOptions.saveState()
            self.neighborOptions.saveState()
        # I don't want stateOptions locking up, so I can't lock this up too.
        super().loadState(state)
        self.stateOptions.loadState(state)
        self.filterOptions.loadState(state)
        self.neighborOptions.loadState(state)

    # The events in this frame just pass the event up to the main frame. The events are done like this to make the sub
    # Options classes more robust. They only reference their master this way, and not their master's master.
    def __bindEvents(self):
        #This binding passes the event up to the next master
        #Image State Events
        self.bind("<<AddImageState>>",self.__addImageState)
        self.bind("<<UpImageState>>",self.__upImageState)
        self.bind("<<DownImageState>>",self.__downImageState)
        #Imaging Events
        self.bind("<<SubmitFilterOptions>>",self.__submitFilterOptions)
        #Neighbor Analysis Events
        self.bind("<<SubmitNeighborOptions>>",self.__submitNeighborOptions)
        #Cell Focus Panel Events
        self.bind("<<PreviousCell>>",self.__previousCell)
        self.bind("<<NextCell>>",self.__nextCell)
    def __addImageState(self,event):
        self.master.event_generate("<<AddImageState>>")
    def __upImageState(self,event):
        self.master.event_generate("<<UpImageState>>")
    def __downImageState(self,event):
        self.master.event_generate("<<DownImageState>>")
    def __submitFilterOptions(self,event):
        self.master.event_generate("<<SubmitFilterOptions>>")
    def __submitNeighborOptions(self,event):
        self.master.event_generate("<<SubmitNeighborOptions>>")
    # I currently need these to redraw the neighbor image
    def __previousCell(self,event):
        self.master.event_generate("<<PreviousCell>>")
    def __nextCell(self,event):
        self.master.event_generate("<<NextCell>>")


    # grabs number of total loaded states
    def getTotalStatesCount(self):
        return self.master.getTotalStatesCount()





# This one is weird as it deals with multiple states at the same time
class ImageStatePanel(ControlPanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master,state)
        self._createTitleBanner("Image State Options")
        self._createStatusBanner(self._createStatusText())
        self._createAddStateButton(3)
        self._createUpStateButton(4)
        self._createDownStateButton(5)

# Called to load new state
    def loadState(self,state):
        # I don't want this locking up. Adding states has nothing to do with loading images
        super().loadState(state)
        self._loadStatusBannerState()

# These functions are only called for creation
    def _createAddStateButton(self,row):
        self.addStateButton = tk.Button(self,text="Add New",command=self.__addImageState)
        self.addStateButton.grid(row=row,column=0,columnspan=2)
    def _createUpStateButton(self,row):
        self.upStateButton = tk.Button(self,text="Up Image State",command=self.__upImageState)
        self.upStateButton.grid(row=row,column=0,columnspan=2)
    def _createDownStateButton(self,row):
        self.downStateButton = tk.Button(self,text="Down Image State",command=self.__downImageState)
        self.downStateButton.grid(row=row,column=0,columnspan=2)

    # creates text for status text at creation and for updates
    def _createStatusText(self):
        indexInfo = self.master.getTotalStatesCount()
        return str("Loaded Image State: " + str(indexInfo[0]+1) + "\tTotal Image States: " + str(indexInfo[1]))

# This function is called each time a state is loaded
    def _loadStatusBannerState(self):
        self.statusLabel.config(text=self._createStatusText())

# These functions only call up to the parent
    def __addImageState(self):
        self.master.event_generate("<<AddImageState>>")
    def __upImageState(self):
        self.master.event_generate("<<UpImageState>>")
    def __downImageState(self):
        self.master.event_generate("<<DownImageState>>")





class FilterOptionsPanel(ControlPanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master,state)

        self._createTitleBanner("Filter Options")
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
            self.state[iST.FILTER_DIAMETER]=self.filterDiameterEntry.get()
            self.state[iST.SIGMA_COLOR]=self.sigmaColorEntry.get()
            self.state[iST.SIGMA_SPACE]=self.sigmaSpaceEntry.get()
            self.state[iST.ADAPTIVE_BLOCKSIZE]=self.adaptiveBlockSizeEntry.get()





class NeighborOptionsPanel(ControlPanel):
    def __init__(self,master=None, state=iS.imageState.copy()):
        super().__init__(master,state)

        self._createTitleBanner("Neighbor Options")
        self._createDeviationOption(2)
        self._createMaxNeighborDistanceOption(3)
        self._createUpperCutoffDistanceOption(4)
        self._createNeighborOptionsSubmitButton(5)

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
        self.deviationEntry.insert(0,"15")
        self.deviationEntry.grid(row=row,column=1)
    def _createMaxNeighborDistanceOption(self,row):
        optionLabel = tk.Label(self,text="Maximum Distance to Neighbors:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.maxNeighborDistanceEntry = tk.Entry(self)
        self.maxNeighborDistanceEntry.insert(0,"80000")
        self.maxNeighborDistanceEntry.grid(row=row,column=1)
    def _createUpperCutoffDistanceOption(self,row):
        optionLabel = tk.Label(self,text="Tree sorting cutoff distance:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.upperCutoffDistanceEntry = tk.Entry(self)
        self.upperCutoffDistanceEntry.insert(0,"75")
        self.upperCutoffDistanceEntry.grid(row=row,column=1)
    def _createNeighborOptionsSubmitButton(self,row):
        optionsSubmitButton = tk.Button(self,text="Submit",command=self.__optionsSubmit)
        optionsSubmitButton.grid(row=row,column=0,columnspan=2)

# These functions are called each time a state is loaded
    def _loadDeviationOptionState(self):
        self.deviationEntry.delete(0,tk.END)
        self.deviationEntry.insert(0,self.state[iST.DEVIATION])
    def _loadMaxNeighborDistanceOptionState(self):
        self.maxNeighborDistanceEntry.delete(0,tk.END)
        self.maxNeighborDistanceEntry.insert(0,self.state[iST.MAX_NEIGHBHOR_DIST])
    def _loadUpperCutoffDistanceOptionState(self):
        self.upperCutoffDistanceEntry.delete(0,tk.END)
        self.upperCutoffDistanceEntry.insert(0,self.state[iST.UPPER_CUTOFF_DIST])

# Saves option data to loaded state before button event activates
    def __optionsSubmit(self):
        self.saveState()
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def saveState(self):
        if super().saveState():
            self.state[iST.DEVIATION]=self.deviationEntry.get()
            self.state[iST.MAX_NEIGHBHOR_DIST]=self.maxNeighborDistanceEntry.get()
            self.state[iST.UPPER_CUTOFF_DIST]=self.upperCutoffDistanceEntry.get()





class CellFocusPanel(ControlPanel):
    def __init__(self,master=None, state=iS.imageState.copy()):
        super().__init__(master,state)

        self._createTitleBanner("Cell Focus Panel")
        self._createStatusBanner(text=self._createStatusText())
        self._createPreviousCellButton(3,0)
        self._createNextCellButton(3,1)

# Called to load new state
    def loadState(self,state):
        if super().loadState(state):
            self._loadStatusBannerState()

    def _createPreviousCellButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Previous",command=self.__previousCell)
        self.addStateButton.grid(row=row,column=column)
    def _createNextCellButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Next",command=self.__nextCell)
        self.addStateButton.grid(row=row,column=column)

    # creates text for status text at creation and for updates
    def _createStatusText(self):
        return str("Cell: " + str(self.state[iST.CELL_INDEX]) + "\tTotal Cells: " + str(len(self.state[iST.CELLS])))

    # Refreshes the Status Banner on changes
    def _loadStatusBannerState(self):
        self.statusLabel.config(text=self._createStatusText())

    # Button Events
    def __previousCell(self):
        # Just a wrapped decrementor
        if (self.state[iST.CELL_INDEX] == 0):
            self.state[iST.CELL_INDEX] = len(self.state[iST.CELLS])
        else:
            self.state[iST.CELL_INDEX] -= 1
        self.master.event_generate("<<PreviousCell>>")
    def __nextCell(self):
        # Just a wrapped incrementor
        if (self.state[iST.CELL_INDEX] == len(self.state[iST.CELLS])):
            self.state[iST.CELL_INDEX] = 0
        else:
            self.state[iST.CELL_INDEX] += 1
        self.master.event_generate("<<NextCell>>")