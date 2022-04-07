########################
##        About       ##
########################
# This panel handles the database
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP

class databasePanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Export Options")
        self._createExportStateButton(3,0)
        self._createExportSuperStateButton(4,0)

    def _createExportStateButton(self,row,column):
        self.exportStateButton = tk.Button(self,text="Export State",command=self.__exportState)
        self.exportStateButton.grid(row=row,column=column)
    def _createExportSuperStateButton(self,row,column):
        self.exportSuperStateButton = tk.Button(self,text="Export Super-State",command=self.__exportSuperState)
        self.exportSuperStateButton.grid(row=row,column=column)

    def __exportState(self):
        self.master.event_generate("<<ExportState>>")
    def __exportSuperState(self):
        self.master.event_generate("<<ExportSuperState>>")