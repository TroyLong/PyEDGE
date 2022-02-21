########################
##        About       ##
########################
# This panel handles the database
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

class databasePanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Database Panel")
        self._createStartAnalysisButton(3,0)

    def _createStartAnalysisButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Export",command=self.__exportDatabase)
        self.addStateButton.grid(row=row,column=column)

    def __exportDatabase(self):
        self.master.event_generate("<<ExportDatabase>>")