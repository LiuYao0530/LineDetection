# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def BGptCount(img, x, y):
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i==0 and j==0:
                continue
            else:
                if(img[x+i][y+j] == 0):
                    count += 1
    return count

def Pattern01Count(img, x, y):
    count = 0
    a = img[x-1][y]
    b = img[x-1][y+1]
    c = img[x][y+1]
    d = img[x+1][y+1]
    e = img[x+1][y]
    f = img[x+1][y-1]
    g = img[x][y-1]
    h = img[x-1][y-1]
    seq = [a,b,c,d,e,f,g,h,a]
    #print seq
    for i in range(0,8):
        if seq[i]==0 and seq[i+1] >0:
            count += 1
    return count

def Condition246(img, x, y):
    p2 = img[x-1][y]
    p4 = img[x][y+1]
    p6 = img[x+1][y]
    if p2*p4*p6==0:
        return True
    else:
        return False

def Condition468(img, x, y):
    p4 = img[x][y+1]
    p6 = img[x+1][y]
    p8 = img[x][y-1]
    if p4*p6*p8 ==0:
        return True
    else:
        return False

def Condition248(img, x, y):
    p2 = img[x-1][y]
    p4 = img[x][y+1]
    p8 = img[x][y-1]
    if p2*p4*p8 ==0:
        return True
    else:
        return False

def Condition268(img, x, y):
    p2 = img[x-1][y]
    p6 = img[x+1][y]
    p8 = img[x][y-1]
    if p2*p6*p8 ==0:
        return True
    else:
        return False


def thin(img, h, w):
    print "h,w",h,w
    c = 0
    res = np.zeros(img.shape)
    all = np.zeros(img.shape)
    for i in range(1, h-1):
        for j in range(1, w-1):
            if img[i][j]==255:
                if (BGptCount(img, i, j)>=2 and BGptCount(img, i, j)<=6)\
                and (Pattern01Count(img, i, j) == 1) and (Condition246(img, i, j) == True)\
                and (Condition468(img, i, j) == True):
                    res[i][j] = 255
                    all[i][j] = 255
                    c += 1
    img = img - res
    if(c == 0):
        return img
    
    c = 0
    res = np.zeros(img.shape)
    for i in range(1, h-1):
        for j in range(1, w-1):
            if img[i][j]==255:
                if (BGptCount(img, i, j)>=2 and BGptCount(img, i, j)<=6)\
                and (Pattern01Count(img, i, j) == 1) and (Condition248(img, i, j) == True)\
                and (Condition268(img, i, j) == True):
                    res[i][j] = 255
                    all[i][j] = 255
                    c += 1
    img = img - res

    if(c == 0):
        return img
    else:
        return thin(img, h, w)

X = []
Y = []
A = np.zeros([29,30])
print type(A)
print A.shape
exit()
for i in range(1,28):
    for j in range(1,29):
        if(j>=1 and j<=9) or (j>=20 and j<=28):
            A[i][j] = 255
            X.append(j)
            Y.append(29-i)
        if(i<=17 and i>=11):
            A[i][j] = 255
            X.append(j)
            Y.append(29-i)
plt.figure(1)
plt.scatter(X,Y,s = 1, c = 'r',marker = 'o')
#print A[26][18]
#print A[26][19]
#print A[26][20]
#print A[27][18]
#print A[27][19]
#print A[27][20]
#print A[28][18]
#print A[28][19]
#print A[28][20]

#print BGptCount(A,27,19)
#print Pattern01Count(A,27,19)
#print Condition246(A,27,19)
#print Condition468(A,27,19)
#print Condition248(A,27,19)
#print Condition268(A,27,19)
print A.shape
print "--------------------------------"

#print thin(A,A.shape[0],A.shape[1])
res = thin(A,A.shape[0],A.shape[1])
AX = []
AY = []
HX = []
HY = []
RX = []
RY = []
for i in range(0,29):
    for j in range(0,30):
        #if(A[i][j] == 255) and (all[i][j] == 255):
        #    AX.append(j)
        #    AY.append(29-i)
        #if(A[i][j] == 255) and (all[i][j] == 0):
        #    HX.append(j)
        #    HY.append(29-i)
        #if(res[i][j] == 255):
        #    AX.append(j)
        #    AY.append(29-i)
        if(res[i][j] == 255):
            RX.append(j)
            RY.append(29-i)

#for i in range(0,29):
#    for j in range(0,30):
#        if(res[i][j]==255):
#            RX.append(j)
#            RY.append(29-i)

plt.figure(2)
plt.scatter(AX,AY,s = 1, c = 'b',marker = 'o')
plt.scatter(HX,HY,s = 1, c = 'r',marker = 'o')
plt.figure(3)
plt.scatter(RX,RY,s = 1, c = 'b',marker = 'o')
plt.show()