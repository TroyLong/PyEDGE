########################
##        About       ##
########################
# This panel displays any important status from the main program
########################
## Imported Libraries ##
########################
import tkinter as tk
import dataTypes.imageState as iS
########################
## Internal Libraries ##
########################
from . import controlPanel as cP


# Displays program status and error messages
class StatusPanel(cP.ControlPanel):
    def __init__(self, master=None, state=None):
        super().__init__(master,state,"Program Status")
    def loadState(self, state):
        super().loadState(state)
        self._updateStatusBanner()
    def _generateStatusText(self):
        #self.statusText += self.master.getStatusMessage()
        return self.statusText