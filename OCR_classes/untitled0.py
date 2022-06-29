# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:37:54 2022

@author: oussa
"""
import cv2
import numpy as np
from skimage.filters import (threshold_otsu, threshold_triangle,
threshold_niblack, threshold_sauvola)
import copy
from skimage import img_as_ubyte

import matplotlib.pyplot as plt

from skimage import measure



image = cv2.imread("IMG3.jpg", 0)

def redimensionnerImage(image,largeur):
    (dimX,dimY) = image.shape
    dimX = int(dimX*largeur/dimY)
    dimY = largeur
    return cv2.resize(image,(dimY,dimX))

image = redimensionnerImage(image,500)



def afficherImage(image):
    #Fonction d'affichage d'une image
    cv2.imshow("Fenetre",image)
    cv2.waitKey(0)
    # cv2.waitKey(2000)
    cv2.destroyAllWindows()

afficherImage(image)


def nettoyerImage(Image):
    thresh_sauvola = threshold_sauvola(Image)
    binary_sauvola = Image > thresh_sauvola
    binary_sauvola = img_as_ubyte(binary_sauvola)
    return binary_sauvola
image = nettoyerImage(image)

afficherImage(image)
print(image.shape)

def calcul_energie(image):
    (l , c) = image.shape
    energy = copy.deepcopy(image)
    for i in range(l):
        for j in range(c):
            energy[i][j] = np.mean(image[i][j:])
    return energy
    
energy = calcul_energie(image)
afficherImage(energy)



def lignes_text(energy, image,voisinage = 1):
    (L , C) = energy.shape
    
    for l in range(0 , L):
        (i , j ) = (l , 0)
        for j in range(C-1):
            if (i >= 1):
                #print(energy[i][j+1])
                if (energy[i][j+1] != 255):
                    i = i - 1
            image[i][j] = 0
            
            
    afficherImage(image)
    
            


lignes_text(energy,image ,voisinage = 1)   