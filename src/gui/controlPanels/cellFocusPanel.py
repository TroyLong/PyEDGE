########################
##        About       ##
########################
# This panel allows the program to focus on one cell and explore its data
########################
## Imported Libraries ##
########################
import tkinter as tk
import dataTypes.state as iS
########################
## Internal Libraries ##
########################
from . import controlPanel as cP


# Selects and retrieves information for induvidual cells
class CellFocusPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Cell Focus Panel")
        self._create_previous(3,0)
        self._create_next(3,1)

    # Called to load new state
    def load(self,state):
        if super().load(state):
            self._update_status()

    # creates text for status text at creation and for updates.
    # Called in _createStatusBanner and _updateStatusBanner()
    def _generate_status(self):
        return str("Cell: " + str(self.state.cell_index) + "\tTotal Cells: " + str(len(self.state.cells)))

    def _create_previous(self,row,column):
        self.previous = tk.Button(self,text="Previous",command=self.__previous_cell)
        self.previous.grid(row=row,column=column)
    def _create_next(self,row,column):
        self.next = tk.Button(self,text="Next",command=self.__next_cell)
        self.next.grid(row=row,column=column)

    # Button Events
    def __previous_cell(self):
        # Just a wrapped decrementor
        if (self.state.cell_index == 0):
            self.state.cell_index = len(self.state.cells)
        else:
            self.state.cell_index -= 1
        self.master.event_generate("<<PreviousCell>>")
    def __next_cell(self):
        # Just a wrapped incrementor
        if (self.state.cell_index == len(self.state.cells)):
            self.state.cell_index = 0
        else:
            self.state.cell_index += 1
        self.master.event_generate("<<NextCell>>")