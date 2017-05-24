import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

picfile = "./line/1.jpg"
img = cv2.imread(picfile)
cv2.imshow("src", img)
img = cv2.medianBlur(img, 11)
cv2.imshow("median", img)
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray_img,30,150)
cv2.imshow("Canny",canny)
cv2.imwrite("median_canny.jpg", canny)
ret,b_img = cv2.threshold(gray_img,170,255,cv2.THRESH_BINARY)
canny = cv2.Canny(b_img,30,150)
cv2.imshow("Canny1",canny)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
dilated = cv2.dilate(b_img, element)
eroded = cv2.erode(dilated, element)
canny = cv2.Canny(eroded,30,150)
cv2.imwrite("threshold_ero_dile_canny.jpg", canny)
cv2.imshow("Canny2",canny)
#dilated = cv2.dilate(eroded, element)

cv2.imshow("Image", b_img)
cv2.imshow("E", eroded)
cv2.imshow("ED", dilated)
cv2.waitKey (0)