import re
from time import time
import cv2 as cv
import analysis
import copy
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
        self.__initKernels()

    # There is a list of states, each of which can be loaded and passed to the whole program
    def __initImageState(self):
        self.timeIndex = 0
        self.zIndex = 0
        self.multiState = [[iS.SingleState()]]
        self.analyzedStates = []
    def __initKernels(self):
        self.kernelWindow = (0,-1)
        self.zKernels = []
        self.kernel = iS.SingleState()

    def openImage(self, imagePath):
        state = iS.SingleState()
        state.openImage(imagePath)
        state.zLevel, state.time = self.reFileNames(imagePath)
        self.multiState[self.timeIndex][self.zIndex] = state
    # opens images to states
    def openImages(self, imagePaths):
        # TODO:: This should house a pattern matching algorithm
        logging.info(f"Opening {len(imagePaths)} files.")
        unsortedStates = []
        for imagePath in imagePaths:
            logging.info(f"Opening: {imagePath}")
            tempState = iS.SingleState()
            # TODO:: should probably be in initializer
            tempState.openImage(imagePath)
            tempState.zLevel, tempState.time = self.reFileNames(imagePath)
            unsortedStates.append(tempState)
            print(f"{unsortedStates[-1].zLevel} {unsortedStates[-1].time}")
        # TODO:: This is just filler for right now
        self.multiState = self.sortImages(unsortedStates)
        logging.info("Finished opening files.\n")
    def reFileNames(self,fileName):
        try:
            fileName = fileName.split("_")
            return int(re.findall(r'\d+',fileName[-2])[0]), int(re.findall(r'\d+',fileName[-1])[0])
        except IndexError:
            return 0,0
    # TODO:: Need to have empty sets for where there are holes
    def sortImages(self, unsortedStates):
        unsortedStates = sorted(unsortedStates,key=lambda state:state.time)
        # TODO:: could probably make this an faster sort
        timeList = [[]]
        lastTime = unsortedStates[0].time
        for state in unsortedStates:
            if state.time == lastTime:
                timeList[-1].append(state)
            else:
                timeList[-1] = sorted(timeList[-1],key=lambda state:state.zLevel)
                timeList.append([state])
            lastTime = state.time
        #exit case
        timeList[-1] = sorted(timeList[-1],key=lambda state:state.zLevel)
        return timeList

    # Time Image State Events
    def addImageStateTime(self):
        self.multiState.append([iS.SingleState()])
    def upImageStateTime(self):
        self.timeIndex += 1 if (self.timeIndex <
                                len(self.multiState)-1) else 0
        self.zIndex = 0
    def downImageStateTime(self):
        self.timeIndex -= 1 if (self.timeIndex>0) else 0
        self.zIndex = 0
    
    # Z Image State Events
    def addImageStateZ(self):
        self.multiState[self.timeIndex].append(iS.SingleState())
    def upImageStateZ(self):
        self.zIndex += 1 if (self.zIndex <
                                len(self.multiState[self.timeIndex])-1) else 0
    def downImageStateZ(self):
        self.zIndex -= 1 if (self.zIndex>0) else 0

    # Imaging Events
    def updateFilterOptions(self):
        self.multiState[self.timeIndex][self.zIndex].updateFilterOptions()
        logging.info(self.multiState[self.timeIndex][self.zIndex])
    def updateAllFilterOptions(self):
        counter = 0
        for timeStates in self.multiState:
            for zLevelState in timeStates:
                print(counter)
                zLevelState.updateFilterOptions()
                counter += 1
    # Neighbor Analysis Events
    def updateNeighborOptions(self):
        self.multiState[self.timeIndex][self.zIndex].updateNeighborOptions()
        logging.info(self.multiState[self.timeIndex][self.zIndex])
    def updateAllNeighborOptions(self):
        for timeStates in self.multiState:
            for zLevelState in timeStates:
                zLevelState.updateNeighborOptions()
                logging.info(zLevelState)


    # TODO:: Not sure if this should be a getter/setter or just a direct variable access
    def updateAnalysisOptions(self,lowAnalysisIndex,highAnalysisIndex):
        self.kernelWindow = lowAnalysisIndex,highAnalysisIndex

    def findKernel(self):
        self.zKernels = []
        for zLevel in self.multiState:
            self.zKernels.append(self.findStateOverlap(zLevel))
        print(type(self.zKernels))
        self.kernel = self.findStateOverlap(self.zKernels,self.kernelWindow[0],self.kernelWindow[1])
        self.kernel.drawCells()
    def findStateOverlap(self,states,index1=0,index2=-1):
        logging.info(f"Starting Union Analysis of {len(states)} states.")
        # Create new stateUnion image from state size and get to the neighbor image
        unionState = iS.SingleState(shape = states[index1].neighbor_image.shape)
        # Fill the stateUnion with the base case.
        # TODO:: Exception catching should occur here
        try:
            unionState.cells = f.findCellOverlap(states[index1].cells, states[index1].cells)
        except IndexError:
            logging.warning("There is a non-proper state invovled in the analysis.")
        # Loop through all image states
        # TODO:: Only loop through a window of indexies to give more user control
        for state in states[index1:index2]:
            unionState.cells = f.findCellOverlap(unionState.cells, state.cells)
        unionState.image_opened = True
        logging.info("finished Union Analysis.")
        logging.info(f"Displaying {len(unionState.cells)} overlapping cells.\n")
        return unionState
        
    def extractCells(self):
        #creates a kernel for each z-level
        kernel = [self.kernel]*len(self.multiState[0])
        self.analyzedStates = []
        for time in self.multiState:
            self.analyzedStates.append([])
            for z,state in enumerate(time):
                # Should update and shift kernel for different zLevels without destroying them
                kernel[z].cells = f.findCellOverlap(kernel[z].cells,state.cells)
                self.analyzedStates[-1].append(copy.copy(kernel[z]))

    # Exports the state
    def exportState(self):
        pandasFunctions.cellsToPandas(
            self.multiState[self.timeIndex][self.zIndex].cells).to_csv("cell.csv")
    def exportSuperState(self):
        pandasFunctions.statesToPandas(self.analyzedStates).to_csv("states.csv")
    # TODO:: Not sure if this should be a getter/setter or just a direct variable access
    # Getters
    def getState(self):
        return self.multiState[self.timeIndex][self.zIndex]
    # This passes information about the number of states, and which is active now
    def getTotalStatesCount(self):
        return (self.timeIndex, len(self.multiState),self.zIndex,len(self.multiState[self.timeIndex]))
