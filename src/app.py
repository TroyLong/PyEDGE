from re import I
from time import time
import analysis
import analysis.filters.cellFilters.cellFilters as cF
import dataTypes.imageState as iS
import multiAnalysis.functions as f
import pandasFunctions


class AppCore:
    def __init__(self):
        print(f"Initializing AppCore: {id(self)}")
        self.__initImageState()
        self.__initStateUnion()

    # There is a list of states, each of which can be loaded and passed to the whole program
    def __initImageState(self):
        self.multiState = [[iS.SingleState()]]
        self.timeIndex = 0
        self.zIndex = 0
        self.state = self.multiState[self.timeIndex][self.zIndex]
        self.statusMessage = ""

    def __initStateUnion(self):
        self.stateUnion = iS.SingleState()

    def openImage(self, imagePaths):
        # TODO:: This should house a pattern matching algorithm
        for imagePath in imagePaths:
            print(f"Opening: {imagePath}")
            if not self.state.image_opened:
                print("Image opened to current state.")
                self.multiState[self.timeIndex][self.zIndex].openImage(imagePath)
            elif self.state.image_opened:
                print("Image opened to new state.")
                self.addImageStateTime()
                self.multiState[self.timeIndex+1][self.zIndex].openImage(imagePath)

    # Time Image State Events
    def addImageStateTime(self):
        self.multiState.append([iS.SingleState()])
    # TODO:: Moves to 0 z index each time for safety. Will work on later
    def upImageStateTime(self):
        self.timeIndex += 1 if (self.timeIndex <
                                len(self.multiState)-1) else 0
        self.zIndex = 0
        self.state = self.multiState[self.timeIndex][self.zIndex]
    def downImageStateTime(self):
        self.timeIndex -= 1 if (self.timeIndex>0) else 0
        self.zIndex = 0
        self.state = self.multiState[self.timeIndex][self.zIndex]
    
    # Z Image State Events
    def addImageStateZ(self):
        self.multiState[self.timeIndex].append(iS.SingleState())
    def upImageStateZ(self):
        self.zIndex += 1 if (self.zIndex <
                                len(self.multiState[self.timeIndex])-1) else 0
        self.state = self.multiState[self.timeIndex][self.zIndex]
    def downImageStateZ(self):
        self.zIndex -= 1 if (self.zIndex>0) else 0
        self.state = self.multiState[self.timeIndex][self.zIndex]

    # Imaging Events
    def updateFilterOptions(self):
        self.multiState[self.timeIndex][self.zIndex].updateFilterOptions()
        print(self.multiState[self.timeIndex][self.zIndex])
    # Neighbor Analysis Events
    def updateNeighborOptions(self):
        self.multiState[self.timeIndex][self.zIndex].updateNeighborOptions()
        print(self.multiState[self.timeIndex][self.zIndex])

    # TODO:: This is just a proof of concept right now
    # Multi state image analysis
    def startStateUnionAnalysis(self):
        # Create new stateUnion image from state size and get to the neighbor image
        self.stateUnion = iS.SingleState(shape = self.multiState[0][0].image.shape)
    
        # Fill the stateUnion with the base case.
        # TODO:: Exception catching should occur here
        self.stateUnion.cells = f.findCellOverlap(
            self.multiState[0][0].cells, self.multiState[0][0].cells)
        # Loop through all image states
        # TODO:: Only loop through a window of indexies to give more user control
        # TODO:: Only looping through top row
        for state in self.multiState:
            self.stateUnion.cells = f.findCellOverlap(
                self.stateUnion.cells, state[0].cells)
        iS.drawCells(self.stateUnion)

    # Exports the state
    def exportState(self):
        pandasFunctions.cellsToPandas(
            self.multiState[self.timeIndex][self.zIndex].cells).to_csv("cell.csv")

    def exportSuperState(self):
        pass
    # Getters

    def getState(self):
        return self.state
    # This passes information about the number of states, and which is active now

    def getTotalStatesCount(self):
        return (self.timeIndex, len(self.multiState),self.zIndex,len(self.multiState[self.timeIndex]))
