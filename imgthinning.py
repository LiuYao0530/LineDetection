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
    #主要要把p2放在序列最后，p9到p2也可以是一个01模式对
    #print seq
    for i in range(0,8):
        if seq[i]==0 and seq[i+1] >0:
            count += 1
    return count

def Condition246(img, x, y):
    p2 = np.long(img[x-1][y])
    p4 = np.long(img[x][y+1])
    p6 = np.long(img[x+1][y])
    if p2*p4*p6==0:
        return True
    else:
        return False

def Condition468(img, x, y):
    p4 = np.long(img[x][y+1])
    p6 = np.long(img[x+1][y])
    p8 = np.long(img[x][y-1])
    if p4*p6*p8 ==0:
        return True
    else:
        return False

def Condition248(img, x, y):
    p2 = np.long(img[x-1][y])
    p4 = np.long(img[x][y+1])
    p8 = np.long(img[x][y-1])
    if p2*p4*p8 ==0:
        return True
    else:
        return False

def Condition268(img, x, y):
    p2 = np.long(img[x-1][y])
    p6 = np.long(img[x+1][y])
    p8 = np.long(img[x][y-1])
    if p2*p6*p8 ==0:
        return True
    else:
        return False


def thin(img, h, w):
    c = 0
    res = np.zeros(img.shape)
    for i in range(1, h-1):
        for j in range(1, w-1):
            if img[i][j]==255:
                if (BGptCount(img, i, j)>=2 and BGptCount(img, i, j)<=6)\
                and (Pattern01Count(img, i, j) == 1) and (Condition246(img, i, j) == True)\
                and (Condition468(img, i, j) == True):
                    res[i][j] = 255
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
                    c += 1
    img = img - res

    if(c == 0):
        return img
    else:
        return thin(img, h, w)

