########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
import dataTypes.imageState as iS
from dataTypes.dataTypeTraits import imageStateTraits as iST

# This is used by all panels and such that are handed the state
class StateMachineFrame(tk.Frame):
    def __init__(self, master=None, state=iS.imageState.copy()):
        super().__init__(master)
        self.master = master
        self.state = state
    # Only loads image if the image is already opened, otherwise it returns a false flag for downstream to deal with
    def loadState(self,state):
        self.state = state
        return self.state[iST.IMAGE_OPENED]
    # Only saves config if the image is already opened, otherwise it returns a false flag for downstream to deal with
    def saveState(self):
        return self.state[iST.IMAGE_OPENED]
    # Allows frame to update without loading a new state
    def update(self):
        pass
    # This sets the state back to the default
    def reset(self):
        self.state=iS.imageState.copy()
    # This creates the title for the machine panel
    def _createTitleBanner(self,text="",fontSize=10,row=1,column=0,columnspan=2):
        bannerLabel = tk.Label(self,text=text)
        bannerLabel.config(font=("Ubuntu",fontSize))
        bannerLabel.grid(row=row,column=column,columnspan=columnspan)