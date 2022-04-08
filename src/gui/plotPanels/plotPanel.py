########################
##        About       ##
########################
# These panels hold visual data such as images or graphs.
########################
## Imported Libraries ##
########################
# Image Analysis Libraries
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
########################
## Internal Libraries ##
########################
import gui.stateMachineFrame as sMF

# PlotPanel parent class for inheritance. Creates figures
class PlotPanel(sMF.StateMachineFrame):
    def __init__(self, master=None,state=None,title = ""):
        super().__init__(master,state)
        self.title = title
        self.__create_title()
        self.__create_figure()
    
    def __create_title(self):
        self.title = tk.Label(self,text=self.title)
        self.title.grid(row=0,column=0)
    
    def __create_figure(self):
        self.figure = plt.Figure(figsize=(3.75,4), dpi=100, tight_layout=True)
        self.figure.format_coord = lambda x, y: ""
        # Canvas for the image or graph to display to
        self.canvas = FigureCanvasTkAgg(self.figure,self)
        # Toolbar has to go in Frame to back with grid
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=2,column=0)
        image_toolbar = NavigationToolbar(self.canvas,toolbar_frame)
        # Adding the canvas to the grid layout manager
        self.canvas.get_tk_widget().grid(row=1,column=0)

    # This is used to make the graph go blank when an empty state is loaded. Otherwise it retains the last graph
    def load_blank_image(self):
        self.figure.clf()
        self.canvas.draw()

# Simpler toolbar
class NavigationToolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]