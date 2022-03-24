########################
##        About       ##
########################
# This frame holds settings for the image processing, and neighbor guessing.
########################
## Internal Libraries ##
########################
import gui.stateMachineFrame as sMF
from gui.controlPanels.statusPanel import StatusPanel
from gui.controlPanels.imageStatePanel import ImageStatePanel
from gui.controlPanels.filterOptionsPanel import FilterOptionsPanel
from gui.controlPanels.neighborOptionsPanel import NeighborOptionsPanel
from gui.controlPanels.cellFocusPanel import CellFocusPanel
from gui.controlPanels.multiStateControl import multiStateAnalysisPanel
from gui.controlPanels.exportPanel import databasePanel
import dataTypes.imageState as iS

# This is the main Panel Window Section
class OptionsZoneFrame(sMF.StateMachineFrame):
    def __init__(self, master=None, state=None):
        super().__init__(master,state)
        self.__bindEvents()
        self.grid()
        self._createTitleBanner("Options",fontSize=14,row=0,columnspan=6)
        self._createStatusPanel(0)
        self._createStatePanel(1)
        self._createFilterOptionsPanel(2)
        self._createNeighborOptionsPanel(3)
        self._createMultiStateAnalysisPanel(4)
        self._createDatabasePanel(5)

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
    def _createMultiStateAnalysisPanel(self,column):
        self.multiStateAnalysisPanel = multiStateAnalysisPanel(self, state=None)
        self.multiStateAnalysisPanel.grid(row=1,column=column,padx=5)
    def _createDatabasePanel(self,column):
        self.databasePanel = databasePanel(self, state=None)
        self.databasePanel.grid(row=1,column=column,padx=5)

    #TODO:: Overwritting the old stuff, and not really running filter any more
    # Called to load new state
    def loadState(self,state):
        self.saveState()
        # I don't want stateOptions locking up, so I can't lock this up too.
        super().loadState(state)
        self.statusPanel.loadState(state)
        self.stateOptions.loadState(state)
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
        self.stateOptions.update()

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
        #Multi state image analysis Events
        self.bind("<<StartMultiStateAnalysis>>",self.__startMultiStateAnalysis)
        #Export Events
        self.bind("<<ExportState>>",self.__exportState)
        self.bind("<<ExportSuperState>>",self.__exportSuperState)

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
    def __startMultiStateAnalysis(self,event):
        self.master.event_generate("<<StartMultiStateAnalysis>>")
    def __exportState(self,event):
        self.master.event_generate("<<ExportState>>")
    def __exportSuperState(self):
        self.master.event_generate("<<ExportSuperState>>")

    # grabs number of total loaded states
    def getTotalStatesCount(self):
        return self.master.getTotalStatesCount()