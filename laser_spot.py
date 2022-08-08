# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 17:12:44 2022

analysis of a laser focal spot
@author: Shou
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from PIL import Image

image = Image.open("3.tif")
image = np.array(image)
# convert to unit8
tracking = image/np.max(image)*255
tracking = tracking.astype(np.uint8)
# grayscale threshold values.
gmn = np.max(tracking)/5
gmx = 253
        
#apply thresholding to grayscale frames. 
ret, thresh = cv2.threshold(tracking, gmn, gmx, 0)

# find contours in the threshold image
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)

# finding contour with maximum area and store it as best_cnt
max_area = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        best_cnt = cnt
# fitting with a ellipse
ellipse = cv2.fitEllipse(best_cnt)
xc = np.int32(ellipse[0][1])
yc = np.int32(ellipse[0][0])
a = ellipse[1][0]
b = ellipse[1][1]
rmax = np.int32(np.max(ellipse[1])*6)

# subtract background
bg = np.mean(tracking[50:150,50:150])
r = np.arange(rmax)
sumr = np.zeros(rmax)
spot0 = tracking[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
spot0 = spot0 - bg
sum0 = np.sum(spot0)

for i in r:
    cv2.circle(spot0,(rmax,rmax),i,(0,0,0),-1)
    sumr[i] = np.sum(spot0)

con = (sum0-sumr)/sum0
plt.plot(r+1,con)
cv2.ellipse(tracking,ellipse,(255,0,0),1) #image ellipse(x0 y0 a b theta) color thickness
spot1 = tracking[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
spot1 = spot1.astype(np.uint8)
cv2.imshow("a",spot1)