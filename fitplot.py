# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imgthinning
from PIL import Image

def prepro(img):
    meadian_img = cv2.medianBlur(img, 11)
    gray_img = cv2.cvtColor(meadian_img,cv2.COLOR_BGR2GRAY)
    print "gray",gray_img.shape
    return gray_img

#将一幅图的边缘提取出来（这里是提取出直线的边缘点来，存为列表，为后面拟合做样本集合）
def contours2ptlist(canny):
    #边缘提取
    _, contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    lineX = []
    lineY = []

    for k in range(len(contours)):
        points = []
        X = []
        Y = []
        alexit = False
        for pt in contours[k][:,0]:
            if len(points) == 0:
                points.append(pt)
                X.append(pt[0])
                Y.append(pt[1])
            else:    
                for b in points:
                    if (pt==b).all():
                        alexit = True
                        break
                if(alexit == False):
                    points.append(pt)
                    X.append(pt[0])
                    Y.append(pt[1])
        YY = [canny.shape[0] - i for i in Y]
        lineX.append(X)
        lineY.append(YY)
    
    return lineX,lineY

picfile = "./line/30000-2.jpg"
img = cv2.imread(picfile)
gray = prepro(img)
h,w = gray.shape

#形态学+边缘细化
ret,b_img = cv2.threshold(gray,170,255,cv2.THRESH_BINARY)
kernel = np.ones((7,7),np.uint8)
closing= cv2.morphologyEx(b_img,cv2.MORPH_GRADIENT,kernel)
#ret,b_img = cv2.threshold(closing,170,255,cv2.THRESH_BINARY)
thin_edge = imgthinning.thin(closing,b_img.shape[0], b_img.shape[1])
#numpy中narray转换成cvMat的问题
#将numpy的数据类型转成cv可以运行的Mat类型,dtype
thin_edgeimg = np.array(thin_edge, dtype = np.uint8)
thin_img = thin_edgeimg.copy()
thin_img_bakcup = thin_img.copy()
#canny
canny = cv2.Canny(gray,30,150)
canny_backup = canny.copy()
img1 = img.copy()
img2 = img.copy()

#概率霍夫变换，找到可能的线段
lines = cv2.HoughLinesP(canny_backup, 8,np.pi/180,30,minLineLength=int(h/3),maxLineGap=8)
#print lines.shape
#print lines
for i in range(0, lines.shape[0]):
    line = lines[i,:,:]
    for x1,y1,x2,y2 in line[:]:
        cv2.line(img1,(x1,y1),(x2,y2),(0,0,255),1)
        cv2.circle(img1,(x1,y1),3,(55,255,155),3)
        cv2.circle(img1,(x2,y2),3,(255,0,155),3)

#概率霍夫变换，找到可能的线段
lines = cv2.HoughLinesP(thin_img_bakcup, 8,np.pi/180,30,minLineLength=int(min(h, w)/4),maxLineGap=5)
#print lines.shape
#print lines
for i in range(0, lines.shape[0]):
    line = lines[i,:,:]
    for x1,y1,x2,y2 in line[:]:
        cv2.line(img2,(x1,y1),(x2,y2),(0,0,255),1)
        cv2.circle(img2,(x1,y1),3,(55,255,155),3)
        cv2.circle(img2,(x2,y2),3,(255,0,155),3)


cv2.imshow("close",closing)
cv2.imshow("b",b_img)
cv2.imshow("thin",thin_edge)
cv2.imshow("c",canny)
cv2.imshow("4",img1)
cv2.imshow("5",img2)
cv2.waitKey(0)
exit()

plt.figure(1)
lineX,lineY = contours2ptlist(canny)
z1 = np.polyfit(lineX[0],lineY[0],1)
p1 = np.poly1d(z1)
z2 = np.polyfit(lineX[1],lineY[1],1)
p2 = np.poly1d(z2)
print "---> canny fit <---"
print p1
print p2
plt.xlim(0, gray.shape[1])
plt.ylim(0, gray.shape[0])
plt.scatter(lineX[0], lineY[0],s = 1, c = 'r',marker = '.')
plt.scatter(lineX[1], lineY[1],s = 1, c = 'r',marker = '.')
plt.plot(lineX[0],p1(lineX[0]),lw=2)
plt.plot(lineX[1],p2(lineX[1]),lw=2)

plt.figure(2)
#numpy中narray转换成cvMat的问题
#将numpy的数据类型转成cv可以运行的Mat类型,dtype
#A = np.array(thin_edge, dtype = np.uint8)
lineX,lineY = contours2ptlist(thin_edgeimg)
z1 = np.polyfit(lineX[0],lineY[0],1)
p1 = np.poly1d(z1)
z2 = np.polyfit(lineX[1],lineY[1],1)
p2 = np.poly1d(z2)
print "---> thinning fit <---"
print p1
print p2
plt.xlim(0, gray.shape[1])
plt.ylim(0, gray.shape[0])
plt.scatter(lineX[0], lineY[0],s = 1, c = 'r',marker = '.')
plt.scatter(lineX[1], lineY[1],s = 1, c = 'r',marker = '.')
plt.plot(lineX[0],p1(lineX[0]),lw=2)
plt.plot(lineX[1],p2(lineX[1]),lw=2)
plt.show()

#cv2.imshow("1",b_img)
#cv2.imshow("2",thin_edge)
#cv2.imshow("canny",canny)
#cv2.waitKey(0)




#截取0.2到0.8部分的图像
small = canny[int(0.2*canny.shape[0]):int(0.8*canny.shape[0]), int(0.2*canny.shape[1]):int(0.8*canny.shape[1])]

#lines = cv2.HoughLinesP(canny_backup, 1,np.pi/180,30,minLineLength=60,maxLineGap=10)
#lines1 = lines[:,0,:]
#for x1,y1,x2,y2 in lines1[:]: 
#    cv2.line(canny_backup,(x1,y1),(x2,y2),(0,0,255),1)
#cv2.imshow("2",canny_backup)


#plt.figure(1)
##plt.xlim(int(0.2*w),int(0.8*w))
##plt.ylim(int(0.2*h),int(0.8*h))
#plt.xlim(0, w)
#plt.ylim(0, h)
#plt.scatter(lineX[0], lineY[0],s = 1, c = 'r',marker = '.')
#plt.scatter(lineX[1], lineY[1],s = 1, c = 'r',marker = '.')
#plt.plot(lineX[1],p1(lineX[1]),lw=2)
#plt.show()


'''
cv2.drawContours(img,contours,1,(0,0,255),1)
#cv2.imshow("Canny",canny)
cv2.imshow("Canny",img)
cv2.waitKey(0)
'''