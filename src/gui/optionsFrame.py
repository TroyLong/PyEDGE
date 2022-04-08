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
        self.__bindEvents()
        self.grid()
        self._create_title("Options",fontSize=14,row=0,columnspan=6)
        self._create_status(0)
        self._create_time_state(0)
        self._create_z_state(1)
        self._create_filter(2)
        self._create_neighbor(3)
        self._create_kernel(4)
        self._create_export(4)

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

    #TODO:: Overwritting the old stuff, and not really running filter any more
    # Called to load new state
    def load(self,state):
        self.save()
        # I don't want stateOptions locking up, so I can't lock this up too.
        super().load(state)
        self.status.load(state)
        self.time_state.load(state)
        self.z_state.load(state)
        self.filter.load(state)
        self.neighbor.load(state)

    def save(self):
        # This insures default settings are saved to previous State if state is changed
        # This does NOT submit the changes for view
        if super().save():
            self.filter.save()
            self.neighbor.save()

    # This allows the panels to refresh with new info without loading a new state
    def update(self):
        self.status.update()
        self.time_state.update()
        self.z_state.update()
        #self.z_state.update

    # The events in this frame just pass the event up to the main frame. The events are done like this to make the sub
    # Options classes more robust. They only reference their master this way, and not their master's master.
    def __bindEvents(self):
        # This binding passes the event up to the next master
        # Time Image State Events
        self.bind("<<AddImageStateTime>>",self.__add_time_state)
        self.bind("<<UpImageStateTime>>",self.__up_time_state)
        self.bind("<<DownImageStateTime>>",self.__down_time_state)
        # Z Image State Events
        self.bind("<<AddImageStateZ>>",self.__add_z_state)
        self.bind("<<UpImageStateZ>>",self.__up_z_state)
        self.bind("<<DownImageStateZ>>",self.__down_z_state)
        #Imaging Events
        self.bind("<<SubmitFilterOptions>>",self.__update_filter)
        self.bind("<<SubmitAllFilterOptions>>",self.__update_all_filters)
        #Neighbor Analysis Events
        self.bind("<<SubmitNeighborOptions>>",self.__update_neighbor_filter)
        self.bind("<<SubmitAllNeighborOptions>>",self.__update_all_neighbor_filters)
        #Cell Focus Panel Events
        self.bind("<<PreviousCell>>",self.__previous_cell)
        self.bind("<<NextCell>>",self.__next_cell)
        #Multi state image analysis Events
        self.bind("<<SubmitKernelWindowOptions>>",self.__update_kernel_window)
        self.bind("<<FindKernel>>",self.__find_kernel)
        self.bind("<<ExtractCells>>",self.__extract_cells)
        #Export Events
        self.bind("<<ExportState>>",self.__export_state)
        self.bind("<<ExportSuperState>>",self.__export_super_state)
    # State Events
    def __add_time_state(self,event):
        self.master.event_generate("<<AddImageStateTime>>")
    def __up_time_state(self,event):
        self.master.event_generate("<<UpImageStateTime>>")
    def __down_time_state(self,event):
        self.master.event_generate("<<DownImageStateTime>>")
    def __add_z_state(self,event):
        self.master.event_generate("<<AddImageStateZ>>")
    def __up_z_state(self,event):
        self.master.event_generate("<<UpImageStateZ>>")
    def __down_z_state(self,event):
        self.master.event_generate("<<DownImageStateZ>>")
    # Filter Events
    def __update_filter(self,event):
        self.master.event_generate("<<SubmitFilterOptions>>")
    def __update_all_filters(self,event):
        self.master.event_generate("<<SubmitAllFilterOptions>>")
    # Neighbor Events
    def __update_neighbor_filter(self,event):
        self.master.event_generate("<<SubmitNeighborOptions>>")
    def __update_all_neighbor_filters(self,event):
        self.master.event_generate("<<SubmitAllNeighborOptions>>")
    # Cell Manipulation Events
    def __previous_cell(self,event):
        self.master.event_generate("<<PreviousCell>>")
    def __next_cell(self,event):
        self.master.event_generate("<<NextCell>>")
    # Kernel Events
    def __update_kernel_window(self,event):
        self.master.event_generate("<<SubmitKernelWindowOptions>>")
    def __find_kernel(self,event):
        self.master.event_generate("<<FindKernel>>")
    def __extract_cells(self,event):
        self.master.event_generate("<<ExtractCells>>")
    # Export Events
    def __export_state(self,event):
        self.master.event_generate("<<ExportState>>")
    def __export_super_state(self,event):
        self.master.event_generate("<<ExportSuperState>>")

    # grabs number of total loaded states
    def get_states_count(self):
        return self.master.get_states_count()
    def get_kernel_window(self):
        return  self.kernel.get_window()