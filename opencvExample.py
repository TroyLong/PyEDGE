import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# This just makes it easier to push an image to display
def showImage(image,title="OpenCV",timeOut=3000):
    cv.namedWindow(title,cv.WINDOW_NORMAL)
    cv.imshow(title,image)
    cv.waitKey(timeOut)
    cv.destroyAllWindows()

#opens the image file
image = cv.imread("twocircles.png")
showImage(image,title="True Color")
#converts the image to grayscale
gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
showImage(gray,title="Gray")
#uses a threshold value to set boundaries for contours
ret, thresh = cv.threshold(gray,100,255,cv.THRESH_BINARY)
showImage(thresh,title="Threshold")
#creates contours around the rings, and fills in with white.
#this may need to be changed as images get "dirtier"
contours,_ = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
filled = thresh.copy()
cv.drawContours(filled,contours, -1, (255,255,255), thickness = cv.FILLED)
showImage(filled,"Filled")


#noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(filled,cv.MORPH_OPEN,kernel, iterations = 2)
#sure background area
sure_bg = cv.dilate(opening,kernel,iterations=3)
showImage(sure_bg,"Sure Background")
#Finding sure foreground area
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,maskSize=5,dstType=cv.CV_8U)
#This will not display correctly
showImage(dist_transform,"Distance Transform")
#This will save the file correctly though
cv.imwrite("distance.png",dist_transform)
ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
showImage(sure_fg,"Sure Foreground")
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
image[markers==-1]=[0,0,255]
showImage(image,title="Final Watershed",timeOut=4000)