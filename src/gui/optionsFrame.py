########################
##        About       ##
########################
# This frame holds settings for the image processing, and neighbor guessing.
########################
## Internal Libraries ##
########################
import gui.stateMachineFrame as sMF
from gui.controlPanels.statusPanel import StatusPanel
from gui.controlPanels.timeStatePanel import TimeStatePanel
from gui.controlPanels.zStatePanel import ZStatePanel
from gui.controlPanels.filterOptionsPanel import FilterOptionsPanel
from gui.controlPanels.neighborOptionsPanel import NeighborOptionsPanel
from gui.controlPanels.cellFocusPanel import CellFocusPanel
from gui.controlPanels.multiStateControl import KernelPanel
from gui.controlPanels.exportPanel import ExportPanel

# This is the main Panel Window Section
class OptionsZoneFrame(sMF.StateMachineFrame):
    def __init__(self, master=None, state=None):
        super().__init__(master,state)
        self.bindEvents()
        self.grid()
        self._create_title("Options",fontSize=14,row=0,columnspan=6)

    # These functions are only called for creation
    def _create_status(self,column):
        self.status = StatusPanel(self,state=self.state)
        self.status.grid(row=2,column=column,padx=5,columnspan=5)
    def _create_time_state(self,column):
        self.time_state = TimeStatePanel(self,state=self.state)
        self.time_state.grid(row=1,column=column,padx=5)
    def _create_z_state(self,column):
        self.z_state = ZStatePanel(self,state=self.state)
        self.z_state.grid(row=1,column=column,padx=5)
    def _create_filter(self,column):
        self.filter = FilterOptionsPanel(self,state=self.state)
        self.filter.grid(row=1,column=column,padx=5)
    def _create_neighbor(self,column):
        self.neighbor = NeighborOptionsPanel(self,state=self.state)
        self.neighbor.grid(row=1,column=column,padx=5)
    def _create_cell_focus(self,column):
        self.cell_focus = CellFocusPanel(self, state=self.state)
        self.cell_focus.grid(row=1,column=column,padx=5)
    def _create_kernel(self,column):
        self.kernel = KernelPanel(self, state=None)
        self.kernel.grid(row=1,column=column,padx=5)
    def _create_export(self,column):
        self.export = ExportPanel(self, state=None)
        self.export.grid(row=2,column=column,padx=5)

    # Called to load new state
    def load(self,state):
        self.save()
        # I don't want stateOptions locking up, so I can't lock this up too.
        super().load(state)        
    def save(self):
        pass
    # This allows the panels to refresh with new info without loading a new state
    def update(self):
        pass

    # The events in this frame just pass the event up to the main frame. The events are done like this to make the sub
    # Options classes more robust. They only reference their master this way, and not their master's master.
    def bindEvents(self):
        # This binding passes the event up to the next master
        # Time Image State Events
        self.bind("<<AddImageStateTime>>",self._add_time_state)
        self.bind("<<UpImageStateTime>>",self._up_time_state)
        self.bind("<<DownImageStateTime>>",self._down_time_state)
        # Z Image State Events
        self.bind("<<AddImageStateZ>>",self._add_z_state)
        self.bind("<<UpImageStateZ>>",self._up_z_state)
        self.bind("<<DownImageStateZ>>",self._down_z_state)
        #Imaging Events
        self.bind("<<SubmitFilterOptions>>",self._update_filter)
        self.bind("<<SubmitAllFilterOptions>>",self._update_all_filters)
        #Neighbor Analysis Events
        self.bind("<<SubmitNeighborOptions>>",self._update_neighbor_filter)
        self.bind("<<SubmitAllNeighborOptions>>",self._update_all_neighbor_filters)
        #Cell Focus Panel Events
        self.bind("<<PreviousCell>>",self._previous_cell)
        self.bind("<<NextCell>>",self._next_cell)
        #Multi state image analysis Events
        self.bind("<<SubmitKernelWindowOptions>>",self._update_kernel_window)
        self.bind("<<FindKernel>>",self._find_kernel)
        self.bind("<<ExtractCells>>",self._extract_cells)
        #Export Events
        self.bind("<<ExportState>>",self._export_state)
        self.bind("<<ExportSuperState>>",self._export_super_state)
    # State Events
    def _add_time_state(self,event):
        self.master.event_generate("<<AddImageStateTime>>")
    def _up_time_state(self,event):
        self.master.event_generate("<<UpImageStateTime>>")
    def _down_time_state(self,event):
        self.master.event_generate("<<DownImageStateTime>>")
    def _add_z_state(self,event):
        self.master.event_generate("<<AddImageStateZ>>")
    def _up_z_state(self,event):
        self.master.event_generate("<<UpImageStateZ>>")
    def _down_z_state(self,event):
        self.master.event_generate("<<DownImageStateZ>>")
    # Filter Events
    def _update_filter(self,event):
        self.master.event_generate("<<SubmitFilterOptions>>")
    def _update_all_filters(self,event):
        self.master.event_generate("<<SubmitAllFilterOptions>>")
    # Neighbor Events
    def _update_neighbor_filter(self,event):
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def _update_all_neighbor_filters(self,event):
        self.master.event_generate("<<SubmitAllNeighborOptions>>")
    # Cell Manipulation Events
    def _previous_cell(self,event):
        self.master.event_generate("<<PreviousCell>>")
    def _next_cell(self,event):
        self.master.event_generate("<<NextCell>>")
    # Kernel Events
    def _update_kernel_window(self,event):
        self.master.event_generate("<<SubmitKernelWindowOptions>>")
    def _find_kernel(self,event):
        self.master.event_generate("<<FindKernel>>")
    def _extract_cells(self,event):
        self.master.event_generate("<<ExtractCells>>")
    # Export Events
    def _export_state(self,event):
        self.master.event_generate("<<ExportState>>")
    def _export_super_state(self,event):
        self.master.event_generate("<<ExportSuperState>>")

    # grabs number of total loaded states
    def get_states_count(self):
        return self.master.get_states_count()
    def get_kernel_window(self):
        return  self.kernel.get_window()