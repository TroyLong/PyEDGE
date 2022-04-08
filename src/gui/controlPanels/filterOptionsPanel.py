########################
##        About       ##
########################
# This panel manipulates image filtering
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import controlPanel as cP

# Controls image filter options
class FilterOptionsPanel(cP.ControlPanel):
    def __init__(self, master=None, state=None):
        super().__init__(master,state,"Filter Options")
        self._create_diameter(2)
        self._create_sigma_color(3)
        self._create_sigma_space(4)
        self._create_adaptive_block_size(5)
        self._create_submit(6)
        self._create_submit_all(7)

    # Called to load new state
    def load(self,state):
        if super().load(state):
            self._load_diameter()
            self._load_sigma_color()
            self._load_sigma_space()
            self._load_adaptive_block_size()

    # These functions are only called for creation
    def _create_diameter(self,row):
        label = tk.Label(self,text="Filter Diameter:")
        label.grid(row=row,column=0,sticky="e")
        self.filter_diameter = tk.Entry(self)
        self.filter_diameter.insert(0,"10")
        self.filter_diameter.grid(row=row,column=1)
    def _create_sigma_color(self,row):
        label = tk.Label(self,text="Bilinear Filter Sigma Color:")
        label.grid(row=row,column=0,sticky="e")
        self.sigma_color = tk.Entry(self)
        self.sigma_color.insert(0,"75")
        self.sigma_color.grid(row=row,column=1)
    def _create_sigma_space(self,row):
        label = tk.Label(self,text="Bilinear Filter Sigma Space:")
        label.grid(row=row,column=0,sticky="e")
        self.sigma_space = tk.Entry(self)
        self.sigma_space.insert(0,"75")
        self.sigma_space.grid(row=row,column=1)
    def _create_adaptive_block_size(self,row):
        label = tk.Label(self,text="Adaptive Threshold Block Size:")
        label.grid(row=row,column=0,sticky="e")
        self.adaptive_block_size = tk.Entry(self)
        self.adaptive_block_size.insert(0,"151")
        self.adaptive_block_size.grid(row=row,column=1)

    def _create_submit(self,row):
        self.submit = tk.Button(self,text="Submit",command=self.__submit)
        self.submit.grid(row=row,column=0,columnspan=2)
    def _create_submit_all(self,row):
        self.submit_all = tk.Button(self,text="Submit All",command=self.__submit_all)
        self.submit_all.grid(row=row,column=0,columnspan=2)
    
    # These functions are called each time a state is loaded
    def _load_diameter(self):
        self.filter_diameter.delete(0,tk.END)
        self.filter_diameter.insert(0,self.state.filter_diameter)
    def _load_sigma_color(self):
        self.sigma_color.delete(0,tk.END)
        self.sigma_color.insert(0,self.state.sigma_color)
    def _load_sigma_space(self):
        self.sigma_space.delete(0,tk.END)
        self.sigma_space.insert(0,self.state.sigma_space)
    def _load_adaptive_block_size(self):
        self.adaptive_block_size.delete(0,tk.END)
        self.adaptive_block_size.insert(0,self.state.adaptive_blocksize)

    # Saves option data to loaded state before button event activates
    def __submit(self):
        self.save()
        self.master.event_generate("<<SubmitFilterOptions>>")
    def __submit_all(self):
        self.save()
        self.master.event_generate("<<SubmitAllFilterOptions>>")
    def save(self):
        if super().save():
            self.state.filter_diameter = int(self._get_entry(self.state.filter_diameter,self.filter_diameter))
            self.state.sigma_color = float(self._get_entry(self.state.sigma_color,self.sigma_color))
            self.state.sigma_space = float(self._get_entry(self.state.sigma_space,self.sigma_space))
            self.state.adaptive_blocksize = int(self._get_entry(self.state.adaptive_blocksize,self.adaptive_block_size))