#TODO:: This is still overwriting 'unsaved' settings on click out
#TODO:: Not running the proper commands. Not being uploaded to the graph correctly

########################
##        About       ##
########################
# These are panels that hold program settings and information
########################
## Imported Libraries ##
########################
import tkinter as tk
import gui.stateMachineFrame as sMF

# ControlPanel parent class for inheritance. Regulates updates to the status banner
class ControlPanel(sMF.StateMachineFrame):
    def __init__(self, master=None, state=None,title = ""):
        super().__init__(master,state)
        # Text that will display in the status box
        self.statusText = ""
        self._createTitleBanner(title)
        self._createStatusBanner()
    def _createStatusBanner(self,row=2,column=0,columnspan=2):
        self.statusLabel = tk.Label(self,text=self._generateStatusText())
        self.statusLabel.grid(row=row,column=column,columnspan=columnspan)
    # Updates panel content without loading new state
    def update(self):
        self._updateStatusBanner()
    def _updateStatusBanner(self):
        self.statusLabel.config(text=self._generateStatusText())
    # Called by _createStatusBanner and _updateStatusBanner
    # Needs to be implemented in subclasses that use the status banner
    def _generateStatusText(self):
        return self.statusText
    # Ensures data entry is float type
    def _getFloatEntry(self,currentValue,entry):
        newValue = 0
        try:
            newValue = float(entry.get())
        except ValueError:
            newValue = currentValue
        return newValue
    # Ensures data entry is int type
    def _getIntEntry(self,currentValue,entry):
        newValue = 0
        try:
            newValue = int(entry.get())
        except ValueError:
            newValue = currentValue
        return newValue