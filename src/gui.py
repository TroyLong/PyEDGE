import tkinter as tk
from tkinter import filedialog as fd
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

        #Unaltered Image from file
        self.originalImageFig = plt.Figure(figsize=(3,4), dpi=100, tight_layout=True)
        self.originalImagePlt = self.originalImageFig.add_subplot(111)
        self.originalImageCanvas = FigureCanvasTkAgg(self.originalImageFig,self)
        self.originalImageCanvas.get_tk_widget().grid(row=0,column=0)
        #Image after going through openCV filters
        self.filteredImageFig = plt.Figure(figsize=(3,4), dpi=100, tight_layout=True)
        self.filteredImagePlt = self.filteredImageFig.add_subplot(111)
        self.filteredImageCanvas = FigureCanvasTkAgg(self.filteredImageFig,self)
        self.filteredImageCanvas.get_tk_widget().grid(row=0,column=1)
        #Drawings of the neighborhood paths
        self.neighborImageFig = plt.Figure(figsize=(3,4), dpi=100, tight_layout=True)
        self.neighborImagePlt = self.neighborImageFig.add_subplot(111)        
        self.neighborImageCanvas = FigureCanvasTkAgg(self.neighborImageFig,self)
        self.neighborImageCanvas.get_tk_widget().grid(row=0,column=2)
        #Histogram of the neighborhood paths
        self.neighborHistFig = plt.Figure(figsize=(3,4), dpi=100, tight_layout=True)
        self.neighborHistPlt = self.neighborHistFig.add_subplot(111)        
        self.neighborHistCanvas = FigureCanvasTkAgg(self.neighborHistFig,self)
        self.neighborHistCanvas.get_tk_widget().grid(row=0,column=3)

        self.textLabel = tk.Label(self,text="Hello, world!")
        self.textLabel.grid(row=1,column=0,columnspan=4)
        

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
        self.__setGraphs()


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
        self.originalImagePlt.imshow(cv.cvtColor(cv.imread(self.imagePath),cv.COLOR_BGR2RGB))
        self.filteredImagePlt.imshow(cv.cvtColor(self.filteredImage,cv.COLOR_BGR2RGB))
        self.neighborImagePlt.imshow(cv.cvtColor(self.filteredImage,cv.COLOR_BGR2RGB))
        self.originalImageCanvas.draw()
        self.filteredImageCanvas.draw()
        self.neighborImageCanvas.draw()

    def __setGraphs(self):
        neighborNumbers = list()
        for cell in self.cells:
            neighborNumbers.append(len(cell[ct.NEIGHBORS]))
        self.neighborHistPlt.hist(neighborNumbers, bins=range(min(neighborNumbers), max(neighborNumbers) + 1, 1))
        self.neighborHistCanvas.draw()





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