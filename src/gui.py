import tkinter as tk
import graphFrame as gf
import topMenu as tm


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.__initApproxConstants()
        self.__bindEvents()
        #Layout manager
        self.grid()
        #Menu bar
        self.topMenuBar = tm.TopMenu(self)
        self.master.config(menu=self.topMenuBar)
        #Frame for graphs
        self.graphFrame = gf.GraphFrame(self,self.deviation,self.maxNeighborDistance,self.upperCutoffDistance)
        self.graphFrame.grid(row=0,column=0)
        #Hello world banner
        self.textLabel = tk.Label(self,text="Hello, world!")
        self.textLabel.grid(row=1,column=0)


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
        self.resetImage()


    def resetImage(self):
        self.graphFrame.resetImage(self.imagePath)






app = App()
app.master.title("PyEDGE")
app.mainloop()