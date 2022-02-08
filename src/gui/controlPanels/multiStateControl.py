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
from dataTypes.dataTypeTraits import imageStateTraits as iST
from . import controlPanel as cP

class multiStateAnalysisPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Multi-State Analysis Panel")
        self._createStartAnalysisButton(3,0)

    def _createStartAnalysisButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Start Analysis",command=self.__startAnalysis)
        self.addStateButton.grid(row=row,column=column)

    def __startAnalysis(self):
        self.master.event_generate("<<StartMultiStateAnalysis>>")