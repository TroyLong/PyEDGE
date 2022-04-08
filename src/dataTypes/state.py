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
import analysis.filters.cellFilters.cellFilters as cF
import analysis.neighborAnalysis as nA
import analysis.segmentImage as sI

# TODO:: Needs to merge with the imageState dictionary to make a slots class
class State(object):
    __slots__ = ("z_level","time","shape","image_opened",
                "image","filtered_image","neighbor_image",
                "cells","cell_index","mean_cell_radii",
                "filter_diameter","sigma_color","sigma_space",
                "adaptive_blocksize","deviation","max_neighbor_dist",
                "upper_cutoff_dist")

    def __init__(self,z_level=0,time=0,shape=None,
                    image=None,neighbor_image=None,cells=None):
        # serializes the time and location of the state for sorting
        self.z_level = z_level
        self.time = time
        # used for loading to gui
        self.image_opened = False
        # dimensions of the image matrix
        self.shape = shape if shape!=None else np.shape((1,1,3))
        # images as np arrays
        self.image = image if image!=None else self.__create_empty_image()
        self.filtered_image = self.__create_empty_image()
        self.neighbor_image = neighbor_image if neighbor_image!=None else self.__create_empty_image()
        # cells
        self.cells = cells if cells!=None else tuple()
        # used to select individual cells
        self.cell_index = 0
        self.mean_cell_radii = 0
        # image filters
        self.filter_diameter = 10
        self.sigma_color = 75
        self.sigma_space = 75
        self.adaptive_blocksize = 151
        # neighbor filters
        self.deviation = 15.0
        self.max_neighbor_dist = 80000.0
        self.upper_cutoff_dist = 5000.0
    # Provides a basic empty image for the default state
    def __create_empty_image(self):
        return np.zeros(self.shape,dtype=np.uint8)

    # Opens and creates images from file
    def open_image(self,imagepath):
        self.image_opened = True
        self.__create_original_image(imagepath)
        self.__create_filtered_image_and_cells()
        self.__create_neighbor_image()

    # Updates state to reflect changes made
    def update_filter(self):
        self.__create_filtered_image_and_cells()
    def update_neighbor_filter(self):
        self.__create_neighbor_image()

    # Creates images from file
    def __create_original_image(self,imagepath):
        self.image = cv.imread(imagepath)
    def __create_filtered_image_and_cells(self):
        # If Adaptive Blocksize is > 2 or %2 = 1 this works. Otherwise I get an error
        self.cells,self.filtered_image = sI.segmentImage(image=self.image,
                                                        diameter=self.filter_diameter,
                                                        bfSigmaColor=self.sigma_color,
                                                        bfSigmaSpace=self.sigma_space,
                                                        atBlockSize=self.adaptive_blocksize)
        #TODO:: I think I should have a more general function call eventually
        self.cells = cF.remove_outlier_small_radii(self,1)
    def __create_neighbor_image(self):
        self.neighbor_image = self.filtered_image.copy()
        nA.process_neighbor_analysis(self)

    ## STATE ANALYSIS FUNCTIONS
    # Finds the mean radii of all the cells in a state
    def find_mean_cell_radii(self):
        average_radius = 0
        for cell in self.cells:
            average_radius += cell.radius
        try:
            return average_radius/(len(self.cells))
        except ZeroDivisionError:
            return 0

    # Caluclates the deviation in cell radii
    # There is probably also a library for this
    def cell_radius_deviation(self):
        deviation = 0
        mean_radius = self.find_mean_cell_radii()
        for cell in self.cells:
            deviation += (cell.radius-mean_radius)**2
        try:
            return np.sqrt(deviation/(len(self.cells)))
        except ZeroDivisionError:
            return 0

    # TODO:: That is grossly written
    def clean_neighbors(self):
        total_mutual = False
        while not total_mutual:
            total_mutual = True            
            for cell in self.cells:
                for neighbor in cell.neighbors:
                    mutual = False
                    for neighbors_neighbor in neighbor.cell.neighbors:
                        if cell == neighbors_neighbor.cell:
                            mutual = True
                    if not mutual:
                        total_mutual = False
                        cell.remove_neighbor(neighbor)

    # Not functional!!!
    def draw_cells(self):
        for cell in self.cells:
            cv.circle(self.neighbor_image,
                    (cell.center[0],cell.center[1]),
                    int(cell.radius),
                    (255, 255, 0),
                    2)

    # Allows printing and loging of this object in a more readable manner
    def __repr__(self):
        return "\n######  STATE PRINTOUT  ######" + \
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
                "\n"
