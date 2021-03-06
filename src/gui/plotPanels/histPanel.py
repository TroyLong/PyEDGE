########################
##        About       ##
########################
# These panels hold visual data such as images or graphs.
########################
## Imported Libraries ##
########################
# Image Analysis Libraries
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
########################
## Internal Libraries ##
########################
from gui.plotPanels import plotPanel as pP


class HistPanel(pP.PlotPanel):
    def __init__(self, master=None,state=None,title = ""):
        super().__init__(master,state,title)
    
    def load(self,state):
        if super().load(state):
            self.__load_hist()

    def __load_hist(self):
        neighbor_numbers = list()
        # Only draw histogram if there are cells to create it with
        if len(self.state.cells):
            for cell in self.state.cells:
                neighbor_numbers.append(len(cell.neighbors))
            self.figure.clf()
            self.hist_plot = self.figure.add_subplot(111)        
            self.hist_plot.hist(neighbor_numbers, bins=range(min(neighbor_numbers), max(neighbor_numbers) + 1, 1))
            axes = self.figure.gca()
            axes.format_coord = lambda x, y: ''
            self.canvas.draw()