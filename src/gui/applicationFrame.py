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
        self.bindEvents()
        #Layout manager
        self.grid()
        self.createMenuBar()
        self.createGraphFrame()
        self.createOptionsFrame()

    def createMenuBar(self):
        self.topMenuBar = tm.TopMenu(self)
        self.master.config(menu=self.topMenuBar)
    def createGraphFrame(self):
        self.graphFrame = gf.GraphZoneFrame()
        self.graphFrame.grid(row=0,column=0)
    def createOptionsFrame(self):
        self.optionsFrame = of.OptionsZoneFrame()
        self.optionsFrame.grid(row=1,column=0)

    # This is the main event handler     
    def bindEvents(self):
        pass

    # This passes the current state to all dependants
    def load_state_to_all(self):
        self.graphFrame.load(self.appCore.get_state())
        self.optionsFrame.load(self.appCore.get_state())

    # TODO:: I think there is a "cooler" way to do this
    def get_states_count(self):
        return self.appCore.get_states_count()