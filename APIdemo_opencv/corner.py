import cv2
import numpy as np
import sys

img = cv2.imread('../images/track_small.jpg')
cv2.imshow('src', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 23, 0.04)
img[dst>0.01 * dst.max()] = [0, 0, 255]     # draw the corner to red
while (True): 
  cv2.imshow('corners', img)
  if cv2.waitKey(int(1000 / 12)) & 0xff == ord("q"):
    break
cv2.destroyAllWindows()
