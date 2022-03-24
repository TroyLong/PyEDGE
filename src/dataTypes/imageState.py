########################
##        About       ##
########################
# This holds the state information for each image loaded into the main program
########################
## Imported Libraries ##
########################
from re import I
import numpy as np
import cv2 as cv
########################
## Internal Libraries ##
########################
from dataTypes.dataTypeTraits import cellTraits as cT
import analysis.filters.cellFilters.cellFilters as cF
import analysis.neighborAnalysis as nA
import analysis.segmentImage as sI

# TODO:: Needs to merge with the imageState dictionary to make a slots class
class SingleState(object):
    def __init__(self):
        self.image_opened = False
        self.image = self.__createEmptyImage()
        self.filtered_image = self.__createEmptyImage()
        self.neighbor_image = self.__createEmptyImage(),
        self.cells = tuple()
        self.cell_index = 0
        self.mean_cell_radii = 0
        self.filter_diameter = 1
        self.sigma_color = 0
        self.sigma_space = 0
        self.adaptive_blocksize = 3
        self.deviation = 15.0
        self.max_neighbor_dist = 80000.0
        self.upper_cutoff_dist = 5000.0
    
    # Provides a basic empty image for the default state
    def __createEmptyImage(self, shape=np.shape((1,1,3))):
        return np.zeros(shape,dtype=np.uint8)

    
    def openImage(self,imagePath):
        self.image_opened = True
        self.__createOriginalImage(imagePath)
        self.__createFilteredImageAndCells()
        self.__createNeighborImage()

    def updateFilterOptions(self):
        self.__createFilteredImageAndCells()
    def updateNeighborOptions(self):
        self.__createNeighborImage()

    def __createOriginalImage(self,imagePath):
        self.image = cv.imread(imagePath)
    def __createFilteredImageAndCells(self):
        # If Adaptive Blocksize is > 2 or %2 = 1 this works. Otherwise I get an error
        self.cells,self.filtered_image = sI.segmentImage(image=self.image,
                                                        diameter=self.filter_diameter,
                                                        bfSigmaColor=self.sigma_color,
                                                        bfSigmaSpace=self.sigma_space,
                                                        atBlockSize=self.adaptive_blocksize)
        #TODO:: I think I should have a more general function call eventually
        self.cells = cF.removeOutlierSmallRadii(self,1)
    def __createNeighborImage(self):
        self.neighbor_image = self.filtered_image.copy()    
        nA.processNeighborAnalysis(self)


    ## STATE ANALYSIS FUNCTIONS

    # Finds the mean radii of all the cells in a state
    def meanCellRadii(self):
        averageRadius = 0
        for cell in self.cells:
            averageRadius += cell[cT.RADIUS]
        try:
            return averageRadius/(len(self.cells))
        except ZeroDivisionError:
            return 0

    # Caluclates the deviation in cell radii
    # There is probably also a library for this
    def cellRadiusDeviation(self):
        deviation = 0
        meanRadius = self.meanCellRadii()
        for cell in self.cells:
            deviation += (cell[cT.RADIUS]-meanRadius)**2
        try:
            return np.sqrt(deviation/(len(self.cells)))
        except ZeroDivisionError:
            return 0

    # Not functional!!!
    def drawCells(self):
        for cell in self.cells:
            cv.circle(self.neighbor_image,
                    (cell[cT.CENTER][0],cell[cT.CENTER][1]),
                    int(cell[cT.RADIUS]),
                    (255, 255, 0),
                    2)

    
    def __repr__(self):
        return "\n######  STATE PRINTOUT  ######\n" + \
                "\nImage Created:         " + str(self.image_opened) + \
                "\n######  Filter Options  ######" + \
                "\nFilter Diameter:       " + str(self.filter_diameter) + \
                "\nSigma Color:           " + str(self.sigma_color) + \
                "\nSimga Space:           " + str(self.sigma_space) + \
                "\nAdaptive Blocksize:    " + str(self.adaptive_blocksize) + \
                "\n######  Neighbor Options #####" + \
                "\nDeviation:             " + str(self.deviation) + \
                "\nMax Neighbor Distance: " + str(self.max_neighbor_dist) + \
                "\nUpper Cutoff Distance: " + str(self.upper_cutoff_dist) + \
                "\n\n"
