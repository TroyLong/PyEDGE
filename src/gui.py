import tkinter as tk
from tkinter import filedialog as fd
import time
import cv2 as cv
import segmentImage as sI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tree
import walkTree
from cell import cellTraits as ct
import neighborFilters as nf



class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.__initApproxConstants()
        self.__bindEvents()


        self.grid()
        self.topMenuBar = topMenu(self)
        self.master.config(menu=self.topMenuBar)

        # An attempt to get matplot integration
        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure,self)
        self.canvas.get_tk_widget().grid()

        self.textLabel = tk.Label(self,text="Hello, world!")
        self.textLabel.grid()
        

    def __initApproxConstants(self):
        #How far can a center be away from the last center and be in the same set
        self.deviation = 15
        #Sets a longest possible neighbor distance. Really important variable
        self.maxNeighborDistance = 80000
        #Allows a first order approximation to speed up tree branching. Small numbers don't look far enough, large numbers take a long time
        self.upperCutoffDistance = 5000

        
    def __bindEvents(self):
        self.bind("<<OpenFile>>",self.__openImage)
    def __openImage(self,event):
        self.imagePath = self.topMenuBar.openImagePath
        self.reset()




    def reset(self):
        self.__runImageAnalysis()
        self.__setImages()

    def __runImageAnalysis(self):
        self.cells,self.filteredImage = sI.segmentImage(self.imagePath)
        self.__runTreeApprox()
        self.__runNeighborFilters()
        self.__drawNeighborAnalysis()

    def __runTreeApprox(self):
        #This box is the default for the tree geometry
        box = tree.Rectangle(0,0,self.filteredImage.shape[0],self.filteredImage.shape[1])
        #Puts Cutoff length in format of tree cutoffThreshold
        upperCutoff = self.filteredImage.shape[1]/self.upperCutoffDistance
        #Creates Tree
        root = tree.treeNode(box,list(self.cells),upperCutoff)
        #Finds neighbors of cells using tree structure
        walkTree.findCloseCells(root,self.cells)

    def __runNeighborFilters(self):
        nf.distanceFilter(self.cells,self.deviation)
        nf.passThroughMultipleAreasFilter(self.cells,self.filteredImage)
    
    def __drawNeighborAnalysis(self):
        for cell in self.cells:
            cv.circle(self.filteredImage, (cell[ct.CENTER][0],cell[ct.CENTER][1]), int(cell[ct.RADIUS]), (255, 255, 0), 2)
            for neighbor in cell[ct.NEIGHBORS]:
                cv.line(self.filteredImage,cell[ct.CENTER],neighbor[ct.CENTER],(132,124,255), 2)


    def __setImages(self):
        newImage = cv.cvtColor(self.filteredImage,cv.COLOR_BGR2RGB)
        self.ax.imshow(newImage)
        self.canvas.draw()





class topMenu(tk.Menu):
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




app = App()
app.master.title("PyEDGE")
app.mainloop()