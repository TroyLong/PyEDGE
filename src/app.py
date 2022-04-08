import re
from time import time
import cv2 as cv
import analysis
import copy
import analysis.filters.cellFilters.cellFilters as cF
import dataTypes.state as s
import multiAnalysis.functions as f
import pandasFunctions
import logging

class AppCore:
    def __init__(self):
        logging.info(f"\n\n------------------------------\n\n" +
                    f"Initializing AppCore: {id(self)}\n")
        self.__init_image_state()
        self.__init_kernels()

    # There is a list of states, each of which can be loaded and passed to the whole program
    def __init_image_state(self):
        self.time_index = 0
        self.z_index = 0
        self.multi_state = [[s.State()]]
        self.analyzed_states = []
    def __init_kernels(self):
        self.kernel_window = (0,-1)
        self.z_kernel = []
        self.kernel = s.State()

    def open_image(self, image_path):
        logging.info(f"Opening: {image_path}...")
        state = s.State()
        state.open_image(image_path)
        state.z_level, state.time = self.re_file_names(image_path)
        self.multi_state[self.time_index][self.z_index] = state
        logging.info("Finished opening file.\n")
    # opens images to states
    def open_images(self, image_paths):
        # TODO:: This should house a pattern matching algorithm
        logging.info(f"Opening {len(image_paths)} files...")
        unsorted_states = []
        for image_path in image_paths:
            logging.info(f"Opening: {image_path}...")
            temp_state = s.State()
            # TODO:: should probably be in initializer
            temp_state.open_image(image_path)
            temp_state.z_level, temp_state.time = self.re_file_names(image_path)
            unsorted_states.append(temp_state)
            #print(f"{unsorted_states[-1].z_level} {unsorted_states[-1].time}")
        # TODO:: This is just filler for right now
        self.multi_state = self.sort_images(unsorted_states)
        logging.info("Finished opening files.\n")
    def re_file_names(self,filename):
        try:
            filename = filename.split("_")
            return int(re.findall(r'\d+',filename[-2])[0]), int(re.findall(r'\d+',filename[-1])[0])
        except IndexError:
            return 0,0
    # TODO:: Need to have empty sets for where there are holes
    def sort_images(self, unsorted_states):
        unsorted_states = sorted(unsorted_states,key=lambda state:state.time)
        # TODO:: could probably make this an faster sort
        time_list = [[]]
        lastTime = unsorted_states[0].time
        for state in unsorted_states:
            if state.time == lastTime:
                time_list[-1].append(state)
            else:
                time_list[-1] = sorted(time_list[-1],key=lambda state:state.z_level)
                time_list.append([state])
            lastTime = state.time
        #exit case
        time_list[-1] = sorted(time_list[-1],key=lambda state:state.z_level)
        return time_list

    # Time Image State Events
    def add_time_state(self):
        self.multi_state.append([s.State()])
    def up_time_state(self):
        self.time_index += 1 if (self.time_index <
                                len(self.multi_state)-1) else 0
        self.z_index = 0
    def down_time_state(self):
        self.time_index -= 1 if (self.time_index>0) else 0
        self.z_index = 0
    
    # Z Image State Events
    def add_z_state(self):
        self.multi_state[self.time_index].append(s.State())
    def up_z_state(self):
        self.z_index += 1 if (self.z_index <
                                len(self.multi_state[self.time_index])-1) else 0
    def down_z_state(self):
        self.z_index -= 1 if (self.z_index>0) else 0

    # Imaging Events
    def update_filter(self):
        self.multi_state[self.time_index][self.z_index].update_filter()
        logging.debug(self.multi_state[self.time_index][self.z_index])
    def update_all_filters(self):
        for time_states in self.multi_state:
            for z_level_state in time_states:
                z_level_state.update_filter()
                logging.debug(z_level_state)
    # Neighbor Analysis Events
    def update_neighbor_filter(self):
        self.multi_state[self.time_index][self.z_index].update_neighbor_filter()
        logging.debug(self.multi_state[self.time_index][self.z_index])
    def update_all_neighbor_filters(self):
        for time_states in self.multi_state:
            for z_level_state in time_states:
                z_level_state.update_neighbor_filter()
                logging.debug(z_level_state)

    # TODO:: Not sure if this should be a getter/setter or just a direct variable access
    def update_kernel_window(self,lowAnalysisIndex,highAnalysisIndex):
        self.kernel_window = lowAnalysisIndex,highAnalysisIndex

    def find_kernel(self):
        self.z_kernel = []
        for z_level in self.multi_state:
            self.z_kernel.append(self.find_state_overlap(z_level))
        self.kernel = self.find_state_overlap(self.z_kernel,self.kernel_window[0],self.kernel_window[1])
        logging.info(f"Kernel formed from window of {self.kernel_window}.\n")
        self.kernel.draw_cells()
    def find_state_overlap(self,states,index1=0,index2=-1):
        logging.info(f"Starting Micro-kernel of {len(states)} states...")
        # Create new stateUnion image from state size and get to the neighbor image
        union_state = s.State(shape = states[index1].neighbor_image.shape)
        # Fill the stateUnion with the base case.
        # TODO:: Exception catching should occur here
        try:
            union_state.cells = f.find_cell_overlap(states[index1].cells, states[index1].cells)
        except IndexError:
            logging.warning("There is a non-proper state invovled in the analysis.")
        # Loop through all image states
        # TODO:: Only loop through a window of indexies to give more user control
        for state in states[index1:index2]:
            union_state.cells = f.find_cell_overlap(union_state.cells, state.cells)
        union_state.image_opened = True
        logging.info(f"Micro-Kernel has {len(union_state.cells)} overlapping cells.")
        return union_state
        
    def extract_cells(self):
        #creates a kernel for each z-level
        kernel = [self.kernel]*len(self.multi_state[0])
        self.analyzed_states = []
        for time in self.multi_state:
            self.analyzed_states.append([])
            for z,state in enumerate(time):
                # Should update and shift kernel for different z_levels without destroying them
                kernel[z].cells = f.find_cell_overlap(kernel[z].cells,state.cells)
                self.analyzed_states[-1].append(copy.copy(kernel[z]))
        logging.info("Extracted cells for data.\n")


    # Exports the state
    def export_state(self):
        logging.info("Exporting active state cells to state.csv...")
        pandasFunctions.cells_to_pandas(
            self.multi_state[self.time_index][self.z_index].cells).to_csv("state.csv")
        logging.info("Export complete.\n")
    def export_super_state(self):
        logging.info("Exporting current extracted cells to states.csv...")
        pandasFunctions.states_to_pandas(self.analyzed_states).to_csv("states.csv")
        logging.info("Export complete...\n")
    # TODO:: Not sure if this should be a getter/setter or just a direct variable access
    # Getters
    def get_state(self):
        return self.multi_state[self.time_index][self.z_index]
    # This passes information about the number of states, and which is active now
    def get_states_count(self):
        return (self.time_index, len(self.multi_state),self.z_index,len(self.multi_state[self.time_index]))
