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

class ExportPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Export Options")
        self._create_export_state(3,0)
        self._create_export_super_state(4,0)

    def _create_export_state(self,row,column):
        self.export_state = tk.Button(self,text="Export State",command=self.__export_state)
        self.export_state.grid(row=row,column=column)
    def _create_export_super_state(self,row,column):
        self.export_super_state = tk.Button(self,text="Export Super-State",command=self.__export_super_state)
        self.export_super_state.grid(row=row,column=column)

    def __export_state(self):
        self.master.event_generate("<<ExportState>>")
    def __export_super_state(self):
        self.master.event_generate("<<ExportSuperState>>")