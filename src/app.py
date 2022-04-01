import re
from time import time
import cv2 as cv
import analysis
import analysis.filters.cellFilters.cellFilters as cF
import dataTypes.imageState as iS
import multiAnalysis.functions as f
import pandasFunctions
import logging

class AppCore:
    def __init__(self):
        logging.info(f"\n\n------------------------------\n\n" +
                    f"Initializing AppCore: {id(self)}\n")
        self.__initImageState()
        self.__initStateUnion()

    # There is a list of states, each of which can be loaded and passed to the whole program
    def __initImageState(self):
        self.unsortedStates = []
        self.multiState = [[iS.SingleState()]]
        self.timeIndex = 0
        self.zIndex = 0
        self.state = self.multiState[self.timeIndex][self.zIndex]
        self.statusMessage = ""

    def __initStateUnion(self):
        self.stateUnion = iS.SingleState()

    def openImage(self, imagePath):
        self.state = iS.SingleState()
        self.state.openImage(imagePath)
        self.state.zLevel, self.state.time = self.reFileNames(imagePath)

    # TODO:: rename as openImages, to bulk open the images then sort multiImage
    # TODO:: create openImage that replaces the current image state
    # opens images to states, but does not sort them!
    def openImages(self, imagePaths):
        # TODO:: This should house a pattern matching algorithm
        logging.info(f"Opening {len(imagePaths)} files.")
        for imagePath in imagePaths:
            logging.info(f"Opening: {imagePath}")
            tempState = iS.SingleState()
            # TODO:: should probably be in initializer
            tempState.openImage(imagePath)
            tempState.zLevel, tempState.time = self.reFileNames(imagePath)
            self.unsortedStates.append(tempState)
            print(f"{self.unsortedStates[-1].zLevel} {self.unsortedStates[-1].time}")
        # TODO:: This is just filler for right now
        self.multiState = [[x] for x in self.unsortedStates]
        logging.info("Finished opening files.\n")

    def sortImages(self):
        pass

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
        logging.info(self.multiState[self.timeIndex][self.zIndex])
    # Neighbor Analysis Events
    def updateNeighborOptions(self):
        self.multiState[self.timeIndex][self.zIndex].updateNeighborOptions()
        logging.info(self.multiState[self.timeIndex][self.zIndex])

    # TODO:: This is just a proof of concept right now
    # Multi state image analysis
    def startStateUnionAnalysis(self):
        logging.info(f"Starting Union Analysis of {len(self.multiState)} states.")
        # Create new stateUnion image from state size and get to the neighbor image
        self.stateUnion = iS.SingleState(shape = self.multiState[0][0].neighbor_image.shape)
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
        self.stateUnion.image_opened = True
        logging.info("finished Union Analysis.")
        logging.info(f"Displaying {len(self.stateUnion.cells)} overlapping cells.\n")
        self.stateUnion.drawCells()

    def reFileNames(self,fileName):
        fileName = fileName.split("_")
        return int(re.findall(r'\d+',fileName[-2])[0]), int(re.findall(r'\d+',fileName[-1])[0])

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
