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
from . import controlPanel as cP

class multiStateAnalysisPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Multi-State Analysis Panel")
        self._createLowAnalysisIndexOption(3,0)
        self._createHighAnalysisIndexOption(4,0)
        self._createSubmitKernelWindowOptionsButton(5,0)
        self._createFindKernelButton(6,0)

    def _createFindKernelButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Find Kernel",command=self.__findKernel)
        self.addStateButton.grid(row=row,column=column,columnspan=2)
    def _createSubmitKernelWindowOptionsButton(self,row,column):
        self.addStateButton = tk.Button(self,text="Submit Window",command=self.__submitKernelWindowOptions)
        self.addStateButton.grid(row=row,column=column,columnspan=2)
        
    def _createLowAnalysisIndexOption(self,row,column):
        optionLabel = tk.Label(self,text="Low Kernel Index:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.lowAnalysisIndexEntry = tk.Entry(self,width=9)
        self.lowAnalysisIndexEntry.insert(0,"0")
        self.lowAnalysisIndexEntry.grid(row=row,column=column+1)
    def _createHighAnalysisIndexOption(self,row,column):
        optionLabel = tk.Label(self,text="High Kernel Index:")
        optionLabel.grid(row=row,column=0,sticky="e")
        self.highAnalysisIndexEntry = tk.Entry(self,width=9)
        self.highAnalysisIndexEntry.insert(0,"-1")
        self.highAnalysisIndexEntry.grid(row=row,column=column+1)
    
    
    def __submitKernelWindowOptions(self):
        self.master.event_generate("<<SubmitKernelWindowOptions>>")
    def __findKernel(self):
        self.master.event_generate("<<FindKernel>>")    
    

    def getAnalysisOptions(self):
        return (self._getIntEntry(0,self.lowAnalysisIndexEntry),
                self._getIntEntry(-1,self.highAnalysisIndexEntry))