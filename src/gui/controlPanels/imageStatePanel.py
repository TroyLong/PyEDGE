########################
##        About       ##
########################
# This panel loads different image states
########################
## Imported Libraries ##
########################
import tkinter as tk
import dataTypes.imageState as iS
########################
## Internal Libraries ##
########################
from . import controlPanel as cP


# This one is weird as it deals with multiple states at the same time
class ImageStatePanel(cP.ControlPanel):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master,state,"Image State Options")
        self._createAddStateButton(3)
        self._createUpStateButton(4)
        self._createDownStateButton(5)

    # Called to load new state
    def loadState(self,state):
        # I don't want this locking up. Adding states has nothing to do with loading images
        super().loadState(state)
        self._updateStatusBanner()

    # creates text for status text at creation and for updates.
    # Called in _createStatusBanner and _updateStatusBanner()
    def _generateStatusText(self):
        indexInfo = self.master.getTotalStatesCount()
        return str("Loaded Image State: " + str(indexInfo[0]+1) + "\tTotal Image States: " + str(indexInfo[1]))

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

    # These functions only call up to the parent
    def __addImageState(self):
        self.master.event_generate("<<AddImageState>>")
    def __upImageState(self):
        self.master.event_generate("<<UpImageState>>")
    def __downImageState(self):
        self.master.event_generate("<<DownImageState>>")