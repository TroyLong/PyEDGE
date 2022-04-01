########################
##        About       ##
########################
# Menubar at top of screen.
########################
## Imported Libraries ##
########################
import tkinter as tk
from tkinter import filedialog as fd


class TopMenu(tk.Menu):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        fileMenu = tk.Menu(self)
        fileMenu.add_command(label="Open Single on State",command=self.openFile)
        fileMenu.add_command(label="Open Multiple Unsorted",command=self.openFiles)
        self.add_cascade(label="File",menu=fileMenu)

        editMenu = tk.Menu(self)
        self.add_cascade(label="Edit",menu=editMenu)

    def openFile(self):
        filetypes = (("tif","*.tif"),("png","*.png"),("gif","*.gif"),("All files","*.*"))
        self.openImagePath = fd.askopenfilename(title="Open an image",initialdir="./",filetypes=filetypes)
        self.master.event_generate("<<OpenFile>>")

    def openFiles(self):
        filetypes = (("tif","*.tif"),("png","*.png"),("gif","*.gif"),("All files","*.*"))
        self.openImagePaths = fd.askopenfilenames(title="Open images",initialdir="./",filetypes=filetypes)
        self.master.event_generate("<<OpenFiles>>")
