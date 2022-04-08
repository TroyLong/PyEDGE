########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from dataTypes.state import State

# This is used by all panels and such that are handed the state
class StateMachineFrame(tk.Frame):
    def __init__(self, master=None, state=None):
        super().__init__(master)
        self.master = master
        self.state = state if state != None else State()
    # Only loads image if the image is already opened, otherwise it returns a false flag for downstream to deal with
    def load(self,state):
        self.state = state
        return self.state.image_opened
    # Only saves config if the image is already opened, otherwise it returns a false flag for downstream to deal with
    def save(self):
        return self.state.image_opened
    # Allows frame to update without loading a new state
    def update(self):
        pass
    # This sets the state back to the default
    def reset(self):
        self.state=State()
    # This creates the title for the machine panel
    def _create_title(self,text="",fontSize=10,row=1,column=0,columnspan=2):
        title = tk.Label(self,text=text)
        title.config(font=("Ubuntu",fontSize))
        title.grid(row=row,column=column,columnspan=columnspan)