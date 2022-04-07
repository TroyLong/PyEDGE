########################
##        About       ##
########################
# This panel loads different image states
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP

# This one is weird as it deals with multiple states at the same time
class TimeStatePanel(cP.ControlPanel):
    def __init__(self, master=None, state=None):
        super().__init__(master,state,"Time State Options")
        self._createAddStateButtonTime()
        self._createUpStateButtonTime()
        self._createDownStateButtonTime()

    # Called to load new state
    def loadState(self,state):
        # I don't want this locking up. Adding states has nothing to do with loading images
        super().loadState(state)
        self._updateStatusBanner()

    # creates text for status text at creation and for updates.
    # Called in _createStatusBanner and _updateStatusBanner()
    def _generateStatusText(self):
        indexInfo = self.master.getTotalStatesCount()
        return f"Loaded Time: {str(indexInfo[0]+1)}    Total Times: {str(indexInfo[1])}"

    # These functions are only called for creation
    def _createAddStateButtonTime(self,column=0,row=3):
        self.addStateButtonTime = tk.Button(self,text="Add Time",command=self.__addImageStateTime)
        self.addStateButtonTime.grid(row=row,column=column,columnspan=2)
    def _createUpStateButtonTime(self,column=0,row=4):
        self.upStateButtonTime = tk.Button(self,text="Up Time State",command=self.__upImageStateTime)
        self.upStateButtonTime.grid(row=row,column=column,columnspan=2)
    def _createDownStateButtonTime(self,column=0,row=5):
        self.downStateButtonTime = tk.Button(self,text="Down Time State",command=self.__downImageStateTime)
        self.downStateButtonTime.grid(row=row,column=column,columnspan=2)


    # These functions only call up to the parent
    def __addImageStateTime(self):
        self.master.event_generate("<<AddImageStateTime>>")
    def __upImageStateTime(self):
        self.master.event_generate("<<UpImageStateTime>>")
    def __downImageStateTime(self):
        self.master.event_generate("<<DownImageStateTime>>")