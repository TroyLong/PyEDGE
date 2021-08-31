import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import disp



#This is really inefficient, but is easy for visualization
#Image for final display
displayImage = [[],[],[]]

#opens the image file
image = cv.imread("onecircle.png")
displayImage[0].append(cv.cvtColor(image,cv.COLOR_BGR2RGB))

#converts the image to grayscale
gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
displayImage[0].append(cv.cvtColor(gray,cv.COLOR_BGR2RGB))

#uses a threshold value to set boundaries for contours
ret, thresh = cv.threshold(gray,100,255,cv.THRESH_BINARY)
displayImage[0].append(cv.cvtColor(thresh,cv.COLOR_BGR2RGB))

#creates contours around the rings, and fills in with white.
#this may need to be changed as images get "dirtier"
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

ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
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
segmentation = image.copy()
segmentation[markers==-1]=[0,0,255]
displayImage[1].append(cv.cvtColor(segmentation,cv.COLOR_BGR2RGB))

ret, segThresh = cv.threshold(gray,100,255,cv.THRESH_BINARY)
segContours,_ = cv.findContours(segThresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
segFilled = segThresh.copy()
cv.drawContours(segFilled,segContours, -1, (255,255,255), thickness = cv.FILLED)
displayImage[2].append(cv.cvtColor(segFilled,cv.COLOR_BGR2RGB))

for c in segContours:
    moment = cv.moments(c)
    # calculate x,y coordinate of center
    cX = int(moment["m10"] / moment["m00"])
    cY = int(moment["m01"] / moment["m00"])
    cv.circle(image, (cX, cY), 1, (0, 0, 255), -1)
displayImage[2].append(cv.cvtColor(image,cv.COLOR_BGR2RGB))


#This took longer than reasonable to put together, but it shows all the
#Images added to the displayImage list
imageLabels = ["Original","Gray","Thresholded","Filled Contour",
                "Sure Background","Distance Transform","Sure Foreground","Segmented Image",
                "Segmented Contour","Centroids"]
fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(8, 8),
                         sharex=True, sharey=True)
ax = axes.ravel()
counter = 0
for i in range(len(displayImage)):
    for j in range(len(displayImage[i])):
        ax[counter].imshow(displayImage[i][j])
        ax[counter].set_title(imageLabels[counter])
        counter+=1
for a in ax:
    a.axis('off')
fig.tight_layout()
plt.show()
