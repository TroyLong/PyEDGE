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
        self.status_text = ""
        self._create_title(title)
        self._create_status()
    def _create_status(self,row=2,column=0,columnspan=2):
        self.status = tk.Label(self,text=self._generate_status())
        self.status.grid(row=row,column=column,columnspan=columnspan)
    # Updates panel content without loading new state
    def update(self):
        self._update_status()
    def _update_status(self):
        self.status.config(text=self._generate_status())
    # Called by _createStatusBanner and _updateStatusBanner
    # Needs to be implemented in subclasses that use the status banner
    def _generate_status(self):
        return self.status_text
    # Protects the entry with a default value
    def _get_entry(self,current_value,entry):
        temp = 0
        try:
            temp = entry.get()
        except ValueError:
            temp = current_value
        return temp