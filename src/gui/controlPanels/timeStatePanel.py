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
        self._create_time_state()
        self._create_up_time_state()
        self._create_down_time_state()

    # Called to load new state
    def load(self,state):
        # I don't want this locking up. Adding states has nothing to do with loading images
        super().load(state)
        self._update_status()

    # creates text for status text at creation and for updates.
    # Called in _createStatusBanner and _updateStatusBanner()
    def _generate_status(self):
        indexInfo = self.master.get_states_count()
        return f"Loaded Time: {str(indexInfo[0]+1)}    Total Times: {str(indexInfo[1])}"

    # These functions are only called for creation
    def _create_time_state(self,column=0,row=3):
        self.add_time_state = tk.Button(self,text="Add Time",command=self.__add_time_state)
        self.add_time_state.grid(row=row,column=column,columnspan=2)
    def _create_up_time_state(self,column=0,row=4):
        self.up_time_state = tk.Button(self,text="Up Time State",command=self.__up_time_state)
        self.up_time_state.grid(row=row,column=column,columnspan=2)
    def _create_down_time_state(self,column=0,row=5):
        self.down_time_state = tk.Button(self,text="Down Time State",command=self.__down_time_state)
        self.down_time_state.grid(row=row,column=column,columnspan=2)


    # These functions only call up to the parent
    def __add_time_state(self):
        self.master.event_generate("<<AddImageStateTime>>")
    def __up_time_state(self):
        self.master.event_generate("<<UpImageStateTime>>")
    def __down_time_state(self):
        self.master.event_generate("<<DownImageStateTime>>")