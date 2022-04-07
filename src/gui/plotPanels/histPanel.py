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
    
    def loadState(self,state):
        if super().loadState(state):
            self.__loadHistState()

    def __loadHistState(self):
        neighborNumbers = list()
        # Only draw histogram if there are cells to create it with
        if len(self.state.cells):
            for cell in self.state.cells:
                neighborNumbers.append(len(cell.neighbors))
            self.plotFig.clf()
            self.histPlt = self.plotFig.add_subplot(111)        
            self.histPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
            axes = self.plotFig.gca()
            axes.format_coord = lambda x, y: ''
            self.plotCanvas.draw()