########################
##        About       ##
########################
# This panel alter neighbor finding parameters
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP


# Controls neighbor finding constraints
class NeighborOptionsPanel(cP.ControlPanel):
    def __init__(self,master=None, state=None):
        super().__init__(master,state,"Neighbor Options")
        self._create_deviation(2)
        self._create_max_neighbor_distance(3)
        self._create_upper_cutoff_distance(4)
        self._create_submit(5)
        self._create_submit_all(6)

    # Called to load new state
    def load(self,state):
        if super().load(state):
            self._load_deviation()
            self._load_max_neighbor_distance()
            self._load_upper_cutoff_distance()
            
    # These functions are only called for creation
    def _create_deviation(self,row):
        label = tk.Label(self,text="Neighbor Distance Deviation:")
        label.grid(row=row,column=0,sticky="e")
        self.deviation = tk.Entry(self)
        self.deviation.insert(0,"15.0")
        self.deviation.grid(row=row,column=1)
    def _create_max_neighbor_distance(self,row):
        label = tk.Label(self,text="Maximum Distance to Neighbors:")
        label.grid(row=row,column=0,sticky="e")
        self.max_neighbor_distance = tk.Entry(self)
        self.max_neighbor_distance.insert(0,"80000.0")
        self.max_neighbor_distance.grid(row=row,column=1)
    def _create_upper_cutoff_distance(self,row):
        label = tk.Label(self,text="Tree sorting cutoff distance:")
        label.grid(row=row,column=0,sticky="e")
        self.upper_cutoff_distance = tk.Entry(self)
        self.upper_cutoff_distance.insert(0,"5000.0")
        self.upper_cutoff_distance.grid(row=row,column=1)
    def _create_submit(self,row):
        submit = tk.Button(self,text="Submit",command=self.__submit)
        submit.grid(row=row,column=0,columnspan=2)
    def _create_submit_all(self,row):
        submit_all = tk.Button(self,text="Submit All",command=self.__submit_all)
        submit_all.grid(row=row,column=0,columnspan=2)

    # These functions are called each time a state is loaded
    def _load_deviation(self):
        self.deviation.delete(0,tk.END)
        self.deviation.insert(0,self.state.deviation)
    def _load_max_neighbor_distance(self):
        self.max_neighbor_distance.delete(0,tk.END)
        self.max_neighbor_distance.insert(0,self.state.max_neighbor_dist)
    def _load_upper_cutoff_distance(self):
        self.upper_cutoff_distance.delete(0,tk.END)
        self.upper_cutoff_distance.insert(0,self.state.upper_cutoff_dist)

    # Saves option data to loaded state before button event activates
    def __submit(self):
        self.save()
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def __submit_all(self):
        self.save()
        self.master.event_generate("<<SubmitAllNeighborOptions>>")
    def save(self):
        if super().save():
            self.state.deviation = float(self._get_entry(self.state.deviation,self.deviation))
            self.state.max_neighbor_dist = float(self._get_entry(self.state.max_neighbor_dist,self.max_neighbor_distance))
            self.state.upper_cutoff_dist = float(self._get_entry(self.state.upper_cutoff_dist,self.upper_cutoff_distance))