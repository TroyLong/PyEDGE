from re import I
import cv2 as cv
import analysis
import analysis.segmentImage as sI
import analysis.neighborAnalysis as nA
import analysis.filters.cellFilters.cellFilters as cF
import dataTypes.imageState as iS
from dataTypes.dataTypeTraits import imageStateTraits as iST
import multiAnalysis.functions as f
import pandasFunctions

class AppCore:
    def __init__(self):
        self.__initImageState()
        self.__initMultiState()

    # There is a list of states, each of which can be loaded and passed to the whole program
    def __initImageState(self):
        self.imageStateIndex = 0
        self.imageStateList = [iS.imageState.copy()]
        self.state = self.imageStateList[self.imageStateIndex]
        self.statusMessage = ""
    def __initMultiState(self):
        self.multiState = iS.imageState.copy()

    def openImage(self,imagePath):
        # TODO:: Is there a shorterway?
        self.state[iST.IMAGE_OPENED] = True
        self.__createOriginalImage(imagePath)
        self.__createFilteredImageAndCells()
        self.__createNeighborImage()


    def __createOriginalImage(self,imagePath):
        self.state[iST.IMAGE] = cv.imread(imagePath)
    def __createFilteredImageAndCells(self):
        # If Adaptive Blocksize is > 2 or %2 = 1 this works. Otherwise I get an error
        self.state[iST.CELLS],self.state[iST.FILTERED_IMAGE] = sI.segmentImage(image=self.state[iST.IMAGE],
                                                                                diameter=self.state[iST.FILTER_DIAMETER],
                                                                                bfSigmaColor=self.state[iST.SIGMA_COLOR],
                                                                                bfSigmaSpace=self.state[iST.SIGMA_SPACE],
                                                                                atBlockSize=self.state[iST.ADAPTIVE_BLOCKSIZE])
        #TODO:: I think I should have a more general function call eventually
        self.state[iST.CELLS] = cF.removeOutlierSmallRadii(self.state,1)
    def __createNeighborImage(self):
        self.state[iST.NEIGHBOR_IMAGE] = self.state[iST.FILTERED_IMAGE].copy()    
        nA.processNeighborAnalysis(self.state)



    # Image State Events
    def addImageState(self):
        self.imageStateList.append(iS.imageState.copy())
    def upImageState(self):
        self.imageStateIndex += 1 if (self.imageStateIndex<len(self.imageStateList)-1) else 0
        self.state = self.imageStateList[self.imageStateIndex]
    def downImageState(self):
        self.imageStateIndex -= 1 if (self.imageStateIndex>0) else 0
        self.state = self.imageStateList[self.imageStateIndex]
    # Imaging Events
    def updateFilterOptions(self):
        self.__createFilteredImageAndCells()
        # TODO:: Perhaps move to test implementation
        iS.printState(self.state)
    # Neighbor Analysis Events
    def updateNeighborOptions(self):
        self.__createNeighborImage()
        iS.printState(self.state)

    # TODO:: This is just a proof of concept right now
    #Multi state image analysis
    def startMultiStateAnalysis(self):
        # I'm comparing the first and last to keep it simple for now
        self.multiState = iS.combinedImageState.copy()
        self.multiState[iST.IMAGE] = iS.createEmptyImage(self.state[iST.IMAGE].shape)
        self.multiState[iST.FILTERED_IMAGE] = iS.createEmptyImage(self.state[iST.IMAGE].shape)
        self.multiState[iST.NEIGHBOR_IMAGE] = iS.createEmptyImage(self.state[iST.IMAGE].shape)
        self.multiState[iST.CELLS] = f.findCellOverlap(self.state[iST.CELLS],self.imageStateList[-1][iST.CELLS])
        iS.drawCells(self.multiState)
        
    #Exports the state
    def exportState(self):
        pandasFunctions.cellsToPandas(self.state[iST.CELLS]).to_csv("cell.csv")
    def exportSuperState(self):
        pass
    # Getters
    def getState(self):
        return self.state
    # This passes information about the number of states, and which is active now
    def getTotalStatesCount(self):
        return (self.imageStateIndex,len(self.imageStateList))