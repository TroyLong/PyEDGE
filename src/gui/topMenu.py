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

        file_menu = tk.Menu(self)
        file_menu.add_command(label="Open Single on State",command=self.open_file)
        file_menu.add_command(label="Open Multiple Unsorted",command=self.open_files)
        self.add_cascade(label="File",menu=file_menu)

        edit_menu = tk.Menu(self)
        self.add_cascade(label="Edit",menu=edit_menu)

    def open_file(self):
        filetypes = (("tif","*.tif"),("png","*.png"),("gif","*.gif"),("All files","*.*"))
        self.open_image_path = fd.askopenfilename(title="Open an image",initialdir="./",filetypes=filetypes)
        self.master.event_generate("<<OpenFile>>")

    def open_files(self):
        filetypes = (("tif","*.tif"),("png","*.png"),("gif","*.gif"),("All files","*.*"))
        self.open_image_paths = fd.askopenfilenames(title="Open images",initialdir="./",filetypes=filetypes)
        self.master.event_generate("<<OpenFiles>>")
