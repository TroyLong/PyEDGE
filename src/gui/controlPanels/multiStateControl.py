########################
##        About       ##
########################
# This panel allows the program to focus on one cell and explore its data
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP

class KernelPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Kernel Panel")
        self._create_window_low(3,0)
        self._create_window_high(4,0)
        self._create_window(5,0)
        self._create_kernel(6,0)
        self._create_extract_cells(7,0)

    def _create_window(self,row,column):
        self.window = tk.Button(self,text="Submit Window",command=self.__submitKernelWindowOptions)
        self.window.grid(row=row,column=column,columnspan=2)
    def _create_kernel(self,row,column):
        self.kernel = tk.Button(self,text="Find Kernel",command=self.__findKernel)
        self.kernel.grid(row=row,column=column,columnspan=2)
    def _create_extract_cells(self,row,column):
        self.extract_cells = tk.Button(self,text="Extract Cells",command=self.__extractCells)
        self.extract_cells.grid(row=row,column=column,columnspan=2)

    def _create_window_low(self,row,column):
        label = tk.Label(self,text="Low Kernel Index:")
        label.grid(row=row,column=0,sticky="e")
        self.window_low = tk.Entry(self,width=9)
        self.window_low.insert(0,"0")
        self.window_low.grid(row=row,column=column+1)
    def _create_window_high(self,row,column):
        label = tk.Label(self,text="High Kernel Index:")
        label.grid(row=row,column=0,sticky="e")
        self.window_high = tk.Entry(self,width=9)
        self.window_high.insert(0,"-1")
        self.window_high.grid(row=row,column=column+1)
    
    
    def __submitKernelWindowOptions(self):
        self.master.event_generate("<<SubmitKernelWindowOptions>>")
    def __findKernel(self):
        self.master.event_generate("<<FindKernel>>")    
    def __extractCells(self):
        self.master.event_generate("<<ExtractCells>>")

    def get_window(self):
        return (int(self._get_entry(0,self.window_low)),
                int(self._get_entry(-1,self.window_high)))