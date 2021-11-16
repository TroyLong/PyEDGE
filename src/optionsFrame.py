#TODO:: I might make an interface for these classes.

# This frame holds settings for the image processing, and neighbor guessing.
# The file currently includes three classes for convienence, but they could be split if need be
import tkinter as tk
import imageState as iS
from imageState import imageStateTraits as iST



class OptionsZoneFrame(tk.Frame):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
        self.__bindEvents()
        self.grid()
        self.__createOptionsLabel()
        self.__createStateOptions(0)
        self.__createFilterOptions(1)
        self.__createNeighborOptions(2)

# These functions are only called for creation
    def __createOptionsLabel(self):
        self.optionsBannerLabel = tk.Label(self,text="Options")
        self.optionsBannerLabel.config(font=("Ubuntu",12))
        self.optionsBannerLabel.grid(row=0,column=0,columnspan=4)
    def __createStateOptions(self,column):
        self.stateOptions = ImageStateOptions(self,state=self.state)
        self.stateOptions.grid(row=1,column=column,padx=5)
    def __createFilterOptions(self,column):
        self.filterOptions = FilterOptions(self,state=self.state)
        self.filterOptions.grid(row=1,column=column,padx=5)
    def __createNeighborOptions(self,column):
        self.neighborOptions = NeighborOptions(self,state=self.state)
        self.neighborOptions.grid(row=1,column=column,padx=5)

    # Called to load new state
    def loadState(self,state):
        self.state = state
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

    # grabs number of total loaded states
    def getTotalStatesCount(self):
        return self.master.getTotalStatesCount()




# This one is weird as it deals with multiple states at the same time
class ImageStateOptions(tk.Frame):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
        self.__createStateOptionsBanner(1)
        self.__createStateStatusBanner(2)
        self.__createAddStateButton(3)
        self.__createUpStateButton(4)
        self.__createDownStateButton(5)

# Called to load new state
    def loadState(self,state):
        self.state = state
        self.__loadStateStatusBannerState()

# These functions are only called for creation
    def __createStateOptionsBanner(self,row):
        bannerLabel = tk.Label(self,text="Image State Options")
        bannerLabel.config(font=("Ubuntu",10))
        bannerLabel.grid(row=row,column=0,columnspan=2)
    def __createStateStatusBanner(self,row):
        indexInfo = self.master.getTotalStatesCount()
        status = "Loaded Image State: " + str(indexInfo[0]) + "\tTotal Image States: " + str(indexInfo[1])
        self.statusLabel = tk.Label(self,text=status)
        self.statusLabel.grid(row=row,column=0,columnspan=2)
    def __createAddStateButton(self,row):
        self.addStateButton = tk.Button(self,text="Add New",command=self.__addImageState)
        self.addStateButton.grid(row=row,column=0,columnspan=2)
    def __createUpStateButton(self,row):
        self.addStateButton = tk.Button(self,text="Up Image State",command=self.__upImageState)
        self.addStateButton.grid(row=row,column=0,columnspan=2)
    def __createDownStateButton(self,row):
        self.addStateButton = tk.Button(self,text="Down Image State",command=self.__downImageState)
        self.addStateButton.grid(row=row,column=0,columnspan=2)

# This function is called each time a state is loaded
    def __loadStateStatusBannerState(self):
        indexInfo = self.master.getTotalStatesCount()
        status = "Loaded Image State: " + str(indexInfo[0]) + "\tTotal Image States: " + str(indexInfo[1])
        self.statusLabel.config(text=status)

# These functions only call up to the parent
    def __addImageState(self):
        self.master.event_generate("<<AddImageState>>")
    def __upImageState(self):
        self.master.event_generate("<<UpImageState>>")
    def __downImageState(self):
        self.master.event_generate("<<DownImageState>>")





class FilterOptions(tk.Frame):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state

        self.__createFilterOptionsBanner(1)
        self.__createFilterDiameterOption(2)
        self.__createSigmaColorOption(3)
        self.__createSigmaSpaceOption(4)
        self.__createAdaptiveBlockSizeOption(5)
        self.__createFilterOptionsSubmit(6)

# Called to load new state
    def loadState(self,state):
        self.state = state
        self.__loadFilterDiameterOptionState()
        self.__loadSigmaColorOptionState()
        self.__loadSigmaSpaceOptionState()
        self.__loadAdaptiveBlockSizeOptionState()

# These functions are only called for creation
    def __createFilterOptionsBanner(self,row):
        bannerLabel = tk.Label(self,text="Filter Options")
        bannerLabel.config(font=("Ubuntu",10))
        bannerLabel.grid(row=row,column=0,columnspan=2)
    def __createFilterDiameterOption(self,row):
        optionLabel = tk.Label(self,text="Filter Diameter:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.filterDiameterEntry = tk.Entry(self)
        self.filterDiameterEntry.insert(0,"10")
        self.filterDiameterEntry.grid(row=row,column=1)
    def __createSigmaColorOption(self,row):
        optionLabel = tk.Label(self,text="Bilinear Filter Sigma Color:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.sigmaColorEntry = tk.Entry(self)
        self.sigmaColorEntry.insert(0,"75")
        self.sigmaColorEntry.grid(row=row,column=1)
    def __createSigmaSpaceOption(self,row):
        optionLabel = tk.Label(self,text="Bilinear Filter Sigma Space:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.sigmaSpaceEntry = tk.Entry(self)
        self.sigmaSpaceEntry.insert(0,"75")
        self.sigmaSpaceEntry.grid(row=row,column=1)
    def __createAdaptiveBlockSizeOption(self,row):
        optionLabel = tk.Label(self,text="Adaptive Threshold Block Size:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.adaptiveBlockSizeEntry = tk.Entry(self)
        self.adaptiveBlockSizeEntry.insert(0,"151")
        self.adaptiveBlockSizeEntry.grid(row=row,column=1)
    def __createFilterOptionsSubmit(self,row):
        self.filterOptionsSubmitButton = tk.Button(self,text="Submit",command=self.__optionsSubmit)
        self.filterOptionsSubmitButton.grid(row=row,column=0,columnspan=2)
    
# These functions are called each time a state is loaded
    def __loadFilterDiameterOptionState(self):
        pass
    def __loadSigmaColorOptionState(self):
        pass
    def __loadSigmaSpaceOptionState(self):
        pass
    def __loadAdaptiveBlockSizeOptionState(self):
        pass

# Saves option data to loaded state before button event activates
    def __optionsSubmit(self):
        self.__saveToState()
        self.master.event_generate("<<SubmitFilterOptions>>")
    def __saveToState(self):
        self.state[iST.FILTER_DIAMETER]=self.filterDiameterEntry.get()
        self.state[iST.SIGMA_COLOR]=self.sigmaColorEntry.get()
        self.state[iST.SIGMA_SPACE]=self.sigmaSpaceEntry.get()
        self.state[iST.ADAPTIVE_BLOCKSIZE]=self.adaptiveBlockSizeEntry.get()





class NeighborOptions(tk.Frame):
    def __init__(self,master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
        self.__createNeighborOptionsBanner(1)
        self.__createDeviationOption(2)
        self.__createMaxNeighborDistanceOption(3)
        self.__createUpperCutoffDistanceOption(4)
        self.__createNeighborOptionsSubmitButton(5)

# Called to load new state
    def loadState(self,state):
        self.state = state
        self.__loadDeviationOptionState()
        self.__loadMaxNeighborDistanceOptionState()
        self.__loadUpperCutoffDistanceOptionState()

# These functions are only called for creation
    def __createNeighborOptionsBanner(self,row):
        bannerLabel = tk.Label(self,text="Neighbor Options")
        bannerLabel.config(font=("Ubuntu",10))
        bannerLabel.grid(row=row,column=0,columnspan=2)
    def __createDeviationOption(self,row):
        optionLabel = tk.Label(self,text="Neighbor Distance Deviation:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.deviationEntry = tk.Entry(self)
        self.deviationEntry.insert(0,"15")
        self.deviationEntry.grid(row=row,column=1)
    def __createMaxNeighborDistanceOption(self,row):
        optionLabel = tk.Label(self,text="Maximum Distance to Neighbors:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.maxNeighborDistanceEntry = tk.Entry(self)
        self.maxNeighborDistanceEntry.insert(0,"80000")
        self.maxNeighborDistanceEntry.grid(row=row,column=1)
    def __createUpperCutoffDistanceOption(self,row):
        optionLabel = tk.Label(self,text="Tree sorting cutoff distance:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.upperCutoffDistanceEntry = tk.Entry(self)
        self.upperCutoffDistanceEntry.insert(0,"75")
        self.upperCutoffDistanceEntry.grid(row=row,column=1)
    def __createNeighborOptionsSubmitButton(self,row):
        optionsSubmitButton = tk.Button(self,text="Submit",command=self.__optionsSubmit)
        optionsSubmitButton.grid(row=row,column=0,columnspan=2)

# These functions are called each time a state is loaded
    def __loadDeviationOptionState(self):
        pass
    def __loadMaxNeighborDistanceOptionState(self):
        pass
    def __loadUpperCutoffDistanceOptionState(self):
        pass

# Saves option data to loaded state before button event activates
    def __optionsSubmit(self):
        self.saveToState()
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def saveToState(self):
        self.state[iST.DEVIATION]=self.deviationEntry.get()
        self.state[iST.MAX_NEIGHBHOR_DIST]=self.maxNeighborDistanceEntry.get()
        self.state[iST.UPPER_CUTOFF_DIST]=self.upperCutoffDistanceEntry.get()