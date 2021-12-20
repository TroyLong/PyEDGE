########################
##        About       ##
########################
# This panel allows the program to focus on one cell and explore its data
########################
## Imported Libraries ##
########################
import tkinter as tk
import dataTypes.imageState as iS
########################
## Internal Libraries ##
########################
from dataTypes.imageState import imageStateTraits as iST
from . import controlPanel as cP


# Selects and retrieves information for induvidual cells
class CellFocusPanel(cP.ControlPanel):
    def __init__(self,master=None, state=iS.imageState.copy()):
        super().__init__(master,state,"Cell Focus Panel")
        self._createPreviousCellButton(3,0)
        self._createNextCellButton(3,1)

    # Called to load new state
    def loadState(self,state):
        if super().loadState(state):
            self._updateStatusBanner()

    # creates text for status text at creation and for updates.
    # Called in _createStatusBanner and _updateStatusBanner()
    def _generateStatusText(self):
        return str("Cell: " + str(self.state[iST.CELL_INDEX]) + "\tTotal Cells: " + str(len(self.state[iST.CELLS])))

    def _createPreviousCellButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Previous",command=self.__previousCell)
        self.addStateButton.grid(row=row,column=column)
    def _createNextCellButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Next",command=self.__nextCell)
        self.addStateButton.grid(row=row,column=column)

    # Button Events
    def __previousCell(self):
        # Just a wrapped decrementor
        if (self.state[iST.CELL_INDEX] == 0):
            self.state[iST.CELL_INDEX] = len(self.state[iST.CELLS])
        else:
            self.state[iST.CELL_INDEX] -= 1
        self.master.event_generate("<<PreviousCell>>")
    def __nextCell(self):
        # Just a wrapped incrementor
        if (self.state[iST.CELL_INDEX] == len(self.state[iST.CELLS])):
            self.state[iST.CELL_INDEX] = 0
        else:
            self.state[iST.CELL_INDEX] += 1
        self.master.event_generate("<<NextCell>>")