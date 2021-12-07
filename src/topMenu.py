########################
##        About       ##
########################
# Menubar at top of screen.
########################
## Imported Libraries ##
########################
# Gui Libraries
import tkinter as tk
from tkinter import filedialog as fd


class TopMenu(tk.Menu):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        fileMenu = tk.Menu(self)
        fileMenu.add_command(label="Open",command=self.openFile)
        self.add_cascade(label="File",menu=fileMenu)

        editMenu = tk.Menu(self)
        self.add_cascade(label="Edit",menu=editMenu)


    def openFile(self):
        filetypes = (("tif","*.tif"),("png","*.png"),("gif","*.gif"),("All files","*.*"))
        self.openImagePath = fd.askopenfilename(title="Open an image",initialdir="./",filetypes=filetypes)
        self.master.event_generate("<<OpenFile>>")
