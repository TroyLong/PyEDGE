########################
##        About       ##
########################
# This frame holds settings for the image processing, and neighbor guessing.
########################
## Internal Libraries ##
########################
import gui.stateMachineFrame as sMF
from gui.controlPanels.statusPanel import StatusPanel
from gui.controlPanels.timeStatePanel import TimeStatePanel
from gui.controlPanels.zStatePanel import ZStatePanel
from gui.controlPanels.filterOptionsPanel import FilterOptionsPanel
from gui.controlPanels.neighborOptionsPanel import NeighborOptionsPanel
from gui.controlPanels.cellFocusPanel import CellFocusPanel
from gui.controlPanels.multiStateControl import multiStateAnalysisPanel
from gui.controlPanels.exportPanel import databasePanel

# This is the main Panel Window Section
class OptionsZoneFrame(sMF.StateMachineFrame):
    def __init__(self, master=None, state=None):
        super().__init__(master,state)
        self.__bindEvents()
        self.grid()
        self._createTitleBanner("Options",fontSize=14,row=0,columnspan=6)
        self._createStatusPanel(0)
        self._createTimeStatePanel(0)
        self._createZStatePanel(1)
        self._createFilterOptionsPanel(2)
        self._createNeighborOptionsPanel(3)
        self._createMultiStateAnalysisPanel(4)
        self._createDatabasePanel(4)

    # These functions are only called for creation
    def _createStatusPanel(self,column):
        self.statusPanel = StatusPanel(self,state=self.state)
        self.statusPanel.grid(row=2,column=column,padx=5,columnspan=5)
    def _createTimeStatePanel(self,column):
        self.timeStateOptions = TimeStatePanel(self,state=self.state)
        self.timeStateOptions.grid(row=1,column=column,padx=5)
    def _createZStatePanel(self,column):
        self.zStateOptions = ZStatePanel(self,state=self.state)
        self.zStateOptions.grid(row=1,column=column,padx=5)
    def _createFilterOptionsPanel(self,column):
        self.filterOptions = FilterOptionsPanel(self,state=self.state)
        self.filterOptions.grid(row=1,column=column,padx=5)
    def _createNeighborOptionsPanel(self,column):
        self.neighborOptions = NeighborOptionsPanel(self,state=self.state)
        self.neighborOptions.grid(row=1,column=column,padx=5)
    def _createCellFocusPanel(self,column):
        self.cellFocusPanel = CellFocusPanel(self, state=self.state)
        self.cellFocusPanel.grid(row=1,column=column,padx=5)
    def _createMultiStateAnalysisPanel(self,column):
        self.multiStateAnalysisPanel = multiStateAnalysisPanel(self, state=None)
        self.multiStateAnalysisPanel.grid(row=1,column=column,padx=5)
    def _createDatabasePanel(self,column):
        self.databasePanel = databasePanel(self, state=None)
        self.databasePanel.grid(row=2,column=column,padx=5)

    #TODO:: Overwritting the old stuff, and not really running filter any more
    # Called to load new state
    def loadState(self,state):
        self.saveState()
        # I don't want stateOptions locking up, so I can't lock this up too.
        super().loadState(state)
        self.statusPanel.loadState(state)
        self.timeStateOptions.loadState(state)
        self.zStateOptions.loadState(state)
        self.filterOptions.loadState(state)
        self.neighborOptions.loadState(state)

    def saveState(self):
        # This insures default settings are saved to previous State if state is changed
        # This does NOT submit the changes for view
        if super().saveState():
            self.filterOptions.saveState()
            self.neighborOptions.saveState()

    # This allows the panels to refresh with new info without loading a new state
    def update(self):
        self.statusPanel.update()
        self.timeStateOptions.update()
        self.zStateOptions.update()
        #self.zStateOptions.update

    # The events in this frame just pass the event up to the main frame. The events are done like this to make the sub
    # Options classes more robust. They only reference their master this way, and not their master's master.
    def __bindEvents(self):
        # This binding passes the event up to the next master
        # Time Image State Events
        self.bind("<<AddImageStateTime>>",self.__addImageStateTime)
        self.bind("<<UpImageStateTime>>",self.__upImageStateTime)
        self.bind("<<DownImageStateTime>>",self.__downImageStateTime)
        # Z Image State Events
        self.bind("<<AddImageStateZ>>",self.__addImageStateZ)
        self.bind("<<UpImageStateZ>>",self.__upImageStateZ)
        self.bind("<<DownImageStateZ>>",self.__downImageStateZ)
        #Imaging Events
        self.bind("<<SubmitFilterOptions>>",self.__submitFilterOptions)
        self.bind("<<SubmitAllFilterOptions>>",self.__submitAllFilterOptions)
        #Neighbor Analysis Events
        self.bind("<<SubmitNeighborOptions>>",self.__submitNeighborOptions)
        self.bind("<<SubmitAllNeighborOptions>>",self.__submitAllNeighborOptions)
        #Cell Focus Panel Events
        self.bind("<<PreviousCell>>",self.__previousCell)
        self.bind("<<NextCell>>",self.__nextCell)
        #Multi state image analysis Events
        self.bind("<<SubmitKernelWindowOptions>>",self.__submitKernelWindowOptions)
        self.bind("<<FindKernel>>",self.__findKernel)
        self.bind("<<ExtractCells>>",self.__extractCells)
        #Export Events
        self.bind("<<ExportState>>",self.__exportState)
        self.bind("<<ExportSuperState>>",self.__exportSuperState)
    # State Events
    def __addImageStateTime(self,event):
        self.master.event_generate("<<AddImageStateTime>>")
    def __upImageStateTime(self,event):
        self.master.event_generate("<<UpImageStateTime>>")
    def __downImageStateTime(self,event):
        self.master.event_generate("<<DownImageStateTime>>")
    def __addImageStateZ(self,event):
        self.master.event_generate("<<AddImageStateZ>>")
    def __upImageStateZ(self,event):
        self.master.event_generate("<<UpImageStateZ>>")
    def __downImageStateZ(self,event):
        self.master.event_generate("<<DownImageStateZ>>")
    # Filter Events
    def __submitFilterOptions(self,event):
        self.master.event_generate("<<SubmitFilterOptions>>")
    def __submitAllFilterOptions(self,event):
        self.master.event_generate("<<SubmitAllNeighborOptions>>")
    # Neighbor Events
    def __submitNeighborOptions(self,event):
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def __submitAllNeighborOptions(self,event):
        self.master.event_generate("<<SubmitAllNeighborOptions>>")
    # Cell Manipulation Events
    def __previousCell(self,event):
        self.master.event_generate("<<PreviousCell>>")
    def __nextCell(self,event):
        self.master.event_generate("<<NextCell>>")
    # Kernel Events
    def __submitKernelWindowOptions(self,event):
        self.master.event_generate("<<SubmitKernelWindowOptions>>")
    def __findKernel(self,event):
        self.master.event_generate("<<FindKernel>>")
    def __extractCells(self,event):
        self.master.event_generate("<<ExtractCells>>")
    # Export Events
    def __exportState(self,event):
        self.master.event_generate("<<ExportState>>")
    def __exportSuperState(self,event):
        self.master.event_generate("<<ExportSuperState>>")

    # grabs number of total loaded states
    def getTotalStatesCount(self):
        return self.master.getTotalStatesCount()
    # TODO:: Awkward
    def getAnalysisOptions(self):
        return  self.multiStateAnalysisPanel.getAnalysisOptions()