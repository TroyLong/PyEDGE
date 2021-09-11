import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
from numpy.lib.function_base import disp


def removeLargeContours(image,contours):
    largest = max(contours,key=cv.contourArea)
    areaOfLargest = cv.contourArea(largest)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    for contour in contours:
        if cv.contourArea(contour) > (areaOfLargest/4):
            cv.drawContours(mask,[contour], -1, 255, thickness = cv.FILLED)
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


#This is really inefficient, but is easy for visualization
#Image for final display
displayImage = [[],[],[]]

#opens the image file
imageDir = "SampleImages/"
imageName = "spidergfpapril12_11_z01_t021.tif"
imagePath = os.path.join(imageDir,imageName)
print("Loading %s."%(imagePath))
image = cv.imread(imagePath)
displayImage[0].append(cv.cvtColor(image,cv.COLOR_BGR2RGB))

#converts the image to grayscale
image = cv.bilateralFilter(image, 8, 175, 175)
gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
displayImage[0].append(cv.cvtColor(gray,cv.COLOR_BGR2RGB))

#uses a threshold value to set boundaries for contours
thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,91,2)
displayImage[0].append(cv.cvtColor(thresh,cv.COLOR_BGR2RGB))

#creates contours around the rings, and fills in with white.
#this may need to be changed as images get "dirtier"
contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
removeContoursTouchingBorders(thresh,contours)
contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)


filled = thresh.copy()
cv.drawContours(filled,contours, -1, (255,255,255), thickness = cv.FILLED)
displayImage[0].append(cv.cvtColor(filled,cv.COLOR_BGR2RGB))

#noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(filled,cv.MORPH_OPEN,kernel, iterations = 2)

#sure background area
sure_bg = cv.dilate(opening,kernel,iterations=3)
displayImage[1].append(cv.cvtColor(sure_bg,cv.COLOR_BGR2RGB))

#Finding sure foreground area
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,maskSize=5,dstType=cv.CV_8U)
#This will not display correctly
displayImage[1].append(cv.cvtColor(dist_transform,cv.COLOR_BGR2RGB))

ret, sure_fg = cv.threshold(dist_transform,0.01*dist_transform.max(),255,0)
displayImage[1].append(cv.cvtColor(sure_fg,cv.COLOR_BGR2RGB))

#Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg,sure_fg)

#Marker labelling
ret, markers = cv.connectedComponents(sure_fg)
#Add one to all labels so that sure background is not 0, but 1
markers = markers+1
#Now, mark the region of unknown with zero
markers[unknown==255] = 0

#Now we watershed
markers = cv.watershed(image,markers)
#segmentation = image.copy()
#segmentation[markers==-1]=[0,0,255]
segmentation = np.zeros_like(image)
segmentation[markers==-1]=[255,255,255]
displayImage[1].append(cv.cvtColor(segmentation,cv.COLOR_BGR2RGB))

gray = cv.cvtColor(segmentation,cv.COLOR_RGB2GRAY)
ret, thresh = cv.threshold(gray,50,255,cv.THRESH_BINARY_INV)
contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
removeLargeContours(thresh,contours)
removeContoursTouchingBorders(thresh,contours)
contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
filled = thresh.copy()
cv.drawContours(filled,contours, -1, (255,0,255), thickness = cv.FILLED)
displayImage[2].append(cv.cvtColor(filled,cv.COLOR_BGR2RGB))

#Grabs all verticies for the shape
verticies = list()
for cnt in range(len(contours)):
    polyEpsilon = 0.05*cv.arcLength(contours[cnt],True)
    polyApprox = cv.approxPolyDP(contours[cnt],polyEpsilon,True)
    verticies.extend(polyApprox)
    cv.polylines(image,[polyApprox],True,(0,255,255))


#Adds the verticies to the original image for viewing
for vert in verticies:
    vert = vert[0]
    cv.circle(image, (vert[0],vert[1]), 2, (255, 0, 0), -1)


#This finds the center of mass
for c in contours:
    moment = cv.moments(c)
    # calculate x,y coordinate of center
    cX = 0
    cY = 0
    try:
        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])
    except ZeroDivisionError:
        pass
    cv.circle(image, (cX, cY), 2, (0, 0, 255), -1)
displayImage[2].append(cv.cvtColor(image,cv.COLOR_BGR2RGB))


#This took longer than reasonable to put together, but it shows all the
#Images added to the displayImage list
imageLabels = ["Original","Gray","Thresholded","Filled Contour",
                "Sure Background","Distance Transform","Sure Foreground","Segmented Image",
                "Threshold","Segmented Contours","Centroids and Vertices",]
fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(8, 8),
                         sharex=True, sharey=True)
ax = axes.ravel()
counter = 0
for i in range(len(displayImage)):
    for j in range(len(displayImage[i])):
        ax[counter].imshow((displayImage[i][j]).astype(np.uint8))
        ax[counter].set_title(imageLabels[counter])
        counter+=1
for a in ax:
    a.axis('off')
fig.tight_layout()
plt.show()
