########################
##        About       ##
########################
# This frame holds settings for the image processing, and neighbor guessing.
########################
## Imported Libraries ##
########################
# State Machine Libraries
import imageState as iS
########################
## Internal Libraries ##
########################
# Control Panel Libraries
from controlPanel import StatusPanel, ImageStatePanel, FilterOptionsPanel, NeighborOptionsPanel, CellFocusPanel

# This is the main Panel Window Section
class OptionsZoneFrame(iS.StateMachinePanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.__bindEvents()
        self.grid()
        self._createTitleBanner("Options",fontSize=12,row=0)
        self._createStatusPanel(0)
        self._createStatePanel(1)
        self._createFilterOptionsPanel(2)
        self._createNeighborOptionsPanel(3)
        self._createCellFocusPanel(4)

    # These functions are only called for creation
    def _createStatusPanel(self,column):
        self.statusPanel = StatusPanel(self,state=self.state)
        self.statusPanel.grid(row=1,column=column,padx=5)
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



