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
class  ZStatePanel(cP.ControlPanel):
    def __init__(self, master=None, state=None):
        super().__init__(master,state,"Z State Options")
        self._create_add_z_state()
        self._create_up_z_state()
        self._create_down_z_state()

    # Called to load new state
    def load(self,state):
        # I don't want this locking up. Adding states has nothing to do with loading images
        super().load(state)
        self._update_status()

    # creates text for status text at creation and for updates.
    # Called in _createStatusBanner and _updateStatusBanner()
    def _generate_status(self):
        indexInfo = self.master.get_states_count()
        return f"Loaded Z: {str(indexInfo[2]+1)}    Total Z: {str(indexInfo[3])}"

    # These functions are only called for creation
    def _create_add_z_state(self,column=0,row=3):
        self.add_z_state = tk.Button(self,text="Add Z",command=self.__add_z_state)
        self.add_z_state.grid(row=row,column=column,columnspan=2)
    def _create_up_z_state(self,column=0,row=4):
        self.up_z_state = tk.Button(self,text="Up Z State",command=self.__up_z_state)
        self.up_z_state.grid(row=row,column=column,columnspan=2)
    def _create_down_z_state(self,column=0,row=5):
        self.down_z_state = tk.Button(self,text="Down Z State",command=self.__down_z_state)
        self.down_z_state.grid(row=row,column=column,columnspan=2)


    # These functions only call up to the parent
    def __add_z_state(self):
        self.master.event_generate("<<AddImageStateZ>>")
    def __up_z_state(self):
        self.master.event_generate("<<UpImageStateZ>>")
    def __down_z_state(self):
        self.master.event_generate("<<DownImageStateZ>>")