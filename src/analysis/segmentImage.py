# TODO:: Does not follow pep8
########################
##        About       ##
########################
# Splits images into cells.
########################
## Imported Libraries ##
########################
import cv2 as cv
import numpy as np
########################
## Internal Libraries ##
########################
from dataTypes.cell import Cell

# This is used get rid of contours that can appear for the black outer regions of the image
def removeLargeContours(image,contours,thresholdHi=4):
    largest = max(contours,key=cv.contourArea)
    areaOfLargest = cv.contourArea(largest)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    for contour in contours:
        area = cv.contourArea(contour)
        if (area > (areaOfLargest/thresholdHi)):
            cv.drawContours(mask,[contour], -1, 255, thickness = cv.FILLED)
    image = cv.bitwise_not(image,image,mask=mask)

# This removes all contours that border the edges of an image
def removeContoursTouchingBorders(image,contours):
    #info about the original image
    imgHeight, imgWidth = image.shape[0],image.shape[1]
    mask = np.zeros(image.shape[:2], dtype="uint8")
    for contour in contours:
        #info about the contour
        x,y,w,h = cv.boundingRect(contour)
        w += x
        h += y
        #does the bounding rectangle touch the edge of the image
        if x == 0 or y == 0 or w == imgWidth or h == imgHeight:
            cv.drawContours(mask,[contour],-1,255,-1)
    image = cv.bitwise_not(image,image,mask=mask)


# Output is a list of cellDictionarys of the form {"vertices":list(),"centers":list(),"areas":list()}
def segmentImage(image,diameter=10,bfSigmaColor=75,bfSigmaSpace=75,atBlockSize=151):
    cells = list()
    #converts the image to grayscale
    image = cv.bilateralFilter(image, d=diameter,sigmaColor=bfSigmaColor, sigmaSpace=bfSigmaSpace)
    gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    #uses a threshold value to set boundaries for contours
    thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,atBlockSize,2)
    contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    removeContoursTouchingBorders(thresh,contours)
    #noise removal
    cleaningKernel = np.ones((7,7),np.uint8)
    opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,cleaningKernel, iterations = 2)
    #watershed marker prep
    backgroundKernel = np.ones((3,3),np.uint8)
    sure_bg = cv.dilate(opening,backgroundKernel,iterations=2)
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,maskSize=5,dstType=cv.CV_8U)
    ret, sure_fg = cv.threshold(dist_transform,0.01*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)
    #Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0
    #Watershedding and segmention
    markers = cv.watershed(image,markers)
    segmentation = np.zeros_like(image)
    segmentation[markers==-1]=[255,255,255]
    #Re-contouring for output information
    gray = cv.cvtColor(segmentation,cv.COLOR_RGB2GRAY)
    ret, thresh = cv.threshold(gray,50,255,cv.THRESH_BINARY_INV)
    contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    removeLargeContours(thresh,contours)
    contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    #Guess the polygon, and note all vertices
    #This finds the center of mass and mark
    for contour in contours:
        #polygon
        polyEpsilon = 0.025*cv.arcLength(contour,True)
        polyApprox = cv.approxPolyDP(contour,polyEpsilon,True)
        #cv.polylines(image,[polyApprox],True,(0,255,255))
        for vert in polyApprox:
            vert = vert[0]
            cv.circle(image, (vert[0],vert[1]), 2, (255, 0, 0), -1)
        #center of mass
        moment = cv.moments(contour)
        cX = 0
        cY = 0
        try:
            cX = int(moment["m10"] / moment["m00"])
            cY = int(moment["m01"] / moment["m00"])
        except ZeroDivisionError:
            pass
        cv.circle(image, (cX, cY), 1, (0, 0, 255), -1)
        cells.append(Cell(center=(cX,cY),verticies=polyApprox,area=cv.contourArea(contour),
                    radius=np.sqrt(cv.contourArea(contour)/np.pi)))
    return tuple(cells), image
    