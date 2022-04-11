# TODO:: The neighbor analysis is continually adding guessed neighbors each time it is run
########################
##        About       ##
########################
# This displays cell images, the filtered image, and the neighbor mappings
# It may also display graphical aids to analyse the date
########################
## Internal Libraries ##
########################
import gui.stateMachineFrame as sMF

class GraphZoneFrame(sMF.StateMachineFrame):
    def __init__(self, master=None,state=None):
        super().__init__(master,state)
        self.create_graphs()
    def load(self,state):
        if super().load(state):
            self.load_images()
        else:
            self.load_blank_images()
    def open_file(self,imagePath):
        self.load_images()
    # These functions create the spaces where the images can be placed
    def create_graphs(self):
        pass
    # These functions load pre-created images to the graphs
    def load_images(self):
        pass
    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def load_blank_images(self):
        pass