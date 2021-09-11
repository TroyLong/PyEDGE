import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
from numpy.lib.function_base import disp

def removeLargeContours(image,contours,thresholdHi=4):
    largest = max(contours,key=cv.contourArea)
    areaOfLargest = cv.contourArea(largest)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    for contour in contours:
        area = cv.contourArea(contour)
        if (area > (areaOfLargest/thresholdHi)):
            if thresholdHi != -1:
                cv.drawContours(mask,[contour], -1, 255, thickness = cv.FILLED)
        else:
            print(area)
    image = cv.bitwise_not(image,image,mask=mask)


def removeContoursTouchingBorders(image,contours):
    imgHeight, imgWidth = image.shape[0],image.shape[1]
    mask = np.zeros(image.shape[:2], dtype="uint8")
    for contour in contours:
        x,y,w,h = cv.boundingRect(contour)
        w += x
        h += y
        if x == 0 or y == 0 or w == imgWidth or h == imgHeight:
            cv.drawContours(mask,[contour],-1,255,-1)
    image = cv.bitwise_not(image,image,mask=mask)



def segmentImage(imagePath):
    vertices = list()
    centers = list()
    image = cv.imread(imagePath)
    #converts the image to grayscale
    image = cv.bilateralFilter(image, 8, 75, 75)
    gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    #uses a threshold value to set boundaries for contours
    thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,351,2)
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
    #Re-contouring
    gray = cv.cvtColor(segmentation,cv.COLOR_RGB2GRAY)
    ret, thresh = cv.threshold(gray,50,255,cv.THRESH_BINARY_INV)
    contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    removeLargeContours(thresh,contours)
    #removeContoursTouchingBorders(thresh,contours)
    contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    #Guess the polygon, and note all vertices
    #This finds the center of mass and mark
    for c in contours:
        #polygon
        polyEpsilon = 0.025*cv.arcLength(c,True)
        polyApprox = cv.approxPolyDP(c,polyEpsilon,True)
        cv.polylines(image,[polyApprox],True,(0,255,255))
        for vert in polyApprox:
            vert = vert[0]
            cv.circle(image, (vert[0],vert[1]), 2, (255, 0, 0), -1)
        vertices.append(polyApprox)
        #center of mass
        moment = cv.moments(c)
        cX = 0
        cY = 0
        try:
            cX = int(moment["m10"] / moment["m00"])
            cY = int(moment["m01"] / moment["m00"])
        except ZeroDivisionError:
            pass
        centers.append((cX,cY))
        cv.circle(image, (cX, cY), 1, (0, 0, 255), -1)
    return {"image":image,"centers":centers,"vertices":vertices}


imageDir = "SampleImages/"
imageName = "spidergfpapril12_11_z01_t021.tif"
imagePath = os.path.join(imageDir,imageName)
info = segmentImage(imagePath)
image = cv.cvtColor(info["image"],cv.COLOR_BGR2RGB)
plt.imshow(image)
plt.show()