import tkinter as tk
from . import graphFrame as gf
from . import optionsFrame as of
from app import AppCore

class CompareFrame(tk.Frame):
    def __init__(self, master=None, appCore=None):
        super().__init__(master,appCore)

    