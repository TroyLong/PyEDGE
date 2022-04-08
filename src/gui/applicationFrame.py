########################
##        About       ##
########################
# The root overhead of the gui.
# It also currently holds the state machine and cards.
# Loads state cards to gui panels, and holds old states for later
########################
## Imported Libraries ##
########################
import tkinter as tk
########################
## Internal Libraries ##
########################
from . import topMenu as tm
from . import graphFrame as gf
from . import optionsFrame as of
from app import AppCore

class AppFrame(tk.Frame):
    def __init__(self, master=None, appCore=None):
        super().__init__(master)
        self.appCore = appCore if appCore != None else AppCore()
        self.__bindEvents()
        #Layout manager
        self.grid()
        #Menu bar
        self.topMenuBar = tm.TopMenu(self)
        self.master.config(menu=self.topMenuBar)
        #Frame for graphs
        self.graphFrame = gf.GraphZoneFrame(self,state=self.appCore.get_state())
        self.graphFrame.grid(row=0,column=0)
        #Options
        self.optionsFrame = of.OptionsZoneFrame(self,state=self.appCore.get_state())
        self.optionsFrame.grid(row=1,column=0)


    # This is the main event handler     
    def __bindEvents(self):
        self.bind("<<OpenFile>>",self.__open_image)
        self.bind("<<OpenFiles>>",self.__open_images)
        # Time Image State Events
        self.bind("<<AddImageStateTime>>",self.__add_time_state)
        self.bind("<<UpImageStateTime>>",self.__up_time_state)
        self.bind("<<DownImageStateTime>>",self.__down_time_state)
        # Z Image State Events
        self.bind("<<AddImageStateZ>>",self.__add_z_state)
        self.bind("<<UpImageStateZ>>",self.__up_z_state)
        self.bind("<<DownImageStateZ>>",self.__down_z_state)
        # Filter Events
        self.bind("<<SubmitFilterOptions>>",self.__update_filter)
        self.bind("<<SubmitAllFilterOptions>>",self.__update_all_filters)
        # Neighbor Events
        self.bind("<<SubmitNeighborOptions>>",self.__update_neighbors)
        self.bind("<<SubmitAllNeighborOptions>>",self.__update_all_neighbors)
        # Kernel Events
        self.bind("<<SubmitKernelWindowOptions>>",self.__update_kernel_window)
        self.bind("<<FindKernel>>",self.__find_kernel)
        self.bind("<<ExtractCells>>",self.__extract_cells)
        # Export Events
        self.bind("<<ExportState>>",self.__export_state)
        self.bind("<<ExportSuperState>>",self.__export_super_state)
    # Opens image from file and loads to current state
    def __open_image(self,event):
        self.appCore.open_image(self.topMenuBar.open_image_path)
        self.__load_state_to_all()
    def __open_images(self,event):
        self.appCore.open_images(self.topMenuBar.open_image_paths)
        self.__load_state_to_all()
    # Time Image State Events
    def __add_time_state(self,event):
        self.appCore.add_time_state()
        # Updates the status display to show new state option
        self.optionsFrame.update()
        #self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])
    def __up_time_state(self,event):
        self.appCore.up_time_state()
        self.__load_state_to_all()
    def __down_time_state(self,event):
        self.appCore.down_time_state()
        self.__load_state_to_all()
     # Z Image State Events
    def __add_z_state(self,event):
        self.appCore.add_z_state()
        # Updates the status display to show new state option
        self.optionsFrame.update()
        #self.optionsFrame.loadState(self.imageStateList[self.imageStateIndex])
    def __up_z_state(self,event):
        self.appCore.up_z_state()
        self.__load_state_to_all()
    def __down_z_state(self,event):
        self.appCore.down_z_state()
        self.__load_state_to_all()
    # Imaging Events
    def __update_filter(self,event):
        self.appCore.update_filter()
        self.graphFrame.update_filter()
    def __update_all_filters(self,event):
        self.appCore.update_all_filters()
        self.graphFrame.update_filter()
    # Neighbor Analysis Events
    def __update_neighbors(self,event):
        self.appCore.update_neighbor_filter()
        self.graphFrame.update_neighbor_filter()
    def __update_all_neighbors(self,event):
        self.appCore.update_all_neighbor_filters()
        self.graphFrame.update_neighbor_filter()
    # processes multiple images against each other
    def __update_kernel_window(self,event):
        self.appCore.kernel_window = self.optionsFrame.get_kernel_window()
    def __find_kernel(self,event):
        self.appCore.find_kernel()
        self.graphFrame.load_kernel_state(self.appCore.kernel)
    def __extract_cells(self,event):
        self.appCore.extract_cells()

    # Export Events
    def __export_state(self,event):
        self.appCore.export_state()
    def __export_super_state(self,event):
        self.appCore.export_super_state()

    # This passes the current state to all dependants
    def __load_state_to_all(self):
        self.graphFrame.load(self.appCore.get_state())
        self.optionsFrame.load(self.appCore.get_state())

    # TODO:: I think there is a "cooler" way to do this
    def get_states_count(self):
        return self.appCore.get_states_count()