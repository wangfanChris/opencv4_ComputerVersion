import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('../images/basil.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# cv2.imshow("after threshold", thresh)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
# cv2.imshow("opening", opening)  #放大看好像噪声除的不好

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)
# cv2.imshow("sure_bg", sure_bg)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)   #TODO 这里是什么原理？
ret2, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)
# cv2.imshow("sure_fg", sure_fg)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg) #两区域相减
# cv2.imshow("unknown", unknown)

# Marker labelling
ret3, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

# 让水漫过栅栏
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

# draw processing
plt.subplot(231), plt.imshow(thresh)
plt.title("thresh"), plt.xticks([]), plt.yticks([])

plt.subplot(232), plt.imshow(opening)
plt.title("opening"), plt.xticks([]), plt.yticks([])

plt.subplot(233), plt.imshow(sure_bg)
plt.title("sure_bg"), plt.xticks([]), plt.yticks([])

plt.subplot(234), plt.imshow(dist_transform)
plt.title("dist_transform"), plt.xticks([]), plt.yticks([])

plt.subplot(235), plt.imshow(markers)
plt.title("markers"), plt.xticks([]), plt.yticks([])

plt.subplot(236), plt.imshow(img)
plt.title("opening"), plt.xticks([]), plt.yticks([])

plt.show()
