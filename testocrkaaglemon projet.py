# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 19:48:45 2022

@author: Hatim NAQOS
"""





import cv2
import numpy as np
from skimage.filters import (threshold_otsu, threshold_triangle,
threshold_niblack, threshold_sauvola)
from keras.models import load_model
from skimage import img_as_ubyte


import matplotlib.pyplot as plt

from skimage import measure





largeur = 700


step = 0


def margeLigne(image):
    return int(image.shape[0]/150)

def margeColonne(image):
    return int(image.shape[1]/150)

def chargerImage(lien, Type = 1):#type = 1 pour couleur 0 pour une image avec niveaux de gris
    if Type == 0:
        return cv2.imread(lien,0) 
    return cv2.imread(lien,1)

def afficherImage(image):
    #Fonction d'affichage d'une image
    cv2.imshow("Fenetre",image)  
    cv2.waitKey(0)
    # cv2.waitKey(2000)
    cv2.destroyAllWindows()

def redimensionnerImage(image,largeur):
    (dimX,dimY) = image.shape
    dimX = int(dimX*largeur/dimY)
    dimY = largeur
    return cv2.resize(image,(dimY,dimX)) #dimX , dimY
    

def inverseValeursImage(image):
    resultat = image.copy()
    for i in range(resultat.shape[0]):
        for j in range(resultat.shape[1]):
            if resultat[i][j] == 0:
                resultat[i][j] = 255
            else:
                resultat[i][j] = 0
    return resultat



    
image1 = chargerImage(r"IMG20.jpg" ,0)

afficherImage(image1)

image1 = redimensionnerImage(image1,largeur)


#(dimX,dimY) = (int(dimX*500/dimY), 500)

#afficherImage(image1)


def nettoyerImage(Image):
    thresh_sauvola = threshold_sauvola(Image)
    binary_sauvola = Image > thresh_sauvola
    binary_sauvola = img_as_ubyte(binary_sauvola)
    return binary_sauvola



def ligneText(image, step):
    liste = []
    cordonnees = []
    images = []
    (dimX,dimY) = image.shape
    marge = margeLigne(image)
    i = 0
    j = 0
    while(i < dimX):
        while(i < dimX and image[i,5] == 255):
            i = i + 1
        debutG = i
        while(j < dimX and image[j,dimY-5] == 255):
            j = j + 1
        debutD = j        
        while(i < dimX and image[i,5] == 0):
            i = i+1
        finG = i
        while(j < dimX and image[j,dimY-5] == 0):
            j = j+1
        finD = j

        
        #print(debutG, debutD , finG, finD)
        
        liste.append((min(debutG, debutD) - 5  , max(finG, finD) + 5 ))  
    i = 0
    while(i < len(liste)-1):
        (d1 , f1) = liste[i]
        (d2 , f2) = liste[i+1]
        if (f1 < d2 and f1 < dimX and d2 < dimX):
            cordonnees.append( ( f1 , d2 ) )
        i = i+1
    #print(liste)
    
    i = 0
    while(i < len(cordonnees)):
        (d,f) = cordonnees[i]
        if(np.mean(image[d:f,:]) < 252):
            images.append( image[d:f,:])
        i= i + 1
    return images
    




image = nettoyerImage(image1)

#image = inverseValeursImage(image)

afficherImage(image)


images =ligneText(image,step)


#LigneT = images[0]








#afficherImage(LigneT)


# Find contours at a constant value of 0.8
#contours = measure.find_contours(LigneT, 0.8)

#print(contours[4])




def imageVide(dim):
    return img_as_ubyte([[255 for i in range(dim[1])] for j in range(dim[0])])

#imgVide = imageVide(LigneT.shape)




def contourIndiceEntier(contours):
    resultats = []
    ensembles = []
    for contour in contours:
        l = contour.shape[0]
        contour = [(int(contour[i][0]) , int(contour[i][1])) for i in range(l)]
        resultats.append(contour)
    for resultat in resultats:
        ensemble = sorted(set(resultat))
        ensembles.append(ensemble)
    return ensembles

#ensembles = contourIndiceEntier(contours)




"""for ensemble in ensembles:
    for couple in ensemble:
        imgVide[couple[0] , couple[1]] = 0"""



#print(len(ensembles))

#print(ensemble)





def estInclu(ensemble1 , ensemble2): # ensemble 1 inclu dans l'ensemble 2 ?
    
    Xensemble1 = [ l[0] for l in ensemble1 ]
    Yensemble1 = [ l[1] for l in ensemble1 ]
    XminEnsemble1 = min(Xensemble1)
    XmaxEnsemble1 = max(Xensemble1)
    YminEnsemble1 = min(Yensemble1)
    YmaxEnsemble1 = max(Yensemble1)
    
    Xensemble2 = [ l[0] for l in ensemble2 ]
    Yensemble2 = [ l[1] for l in ensemble2 ]
    XminEnsemble2 = min(Xensemble2)
    XmaxEnsemble2 = max(Xensemble2)
    YminEnsemble2 = min(Yensemble2)
    YmaxEnsemble2 = max(Yensemble2)        
    if (XminEnsemble1 > XminEnsemble2 and YminEnsemble1 > YminEnsemble2 and XmaxEnsemble1 < XmaxEnsemble2 and YmaxEnsemble1 < YmaxEnsemble2):
        return True
    return False

def indicesEnsemblesInculus(ensembles):
    nbr = len(ensembles)
    indicesInclus = []
    for i in range(nbr):
        for j in range(nbr):
            #print(estInclu(ensembles[i], ensembles[j]) )
            if (i != j and estInclu(ensembles[i], ensembles[j]) ):
                indicesInclus.append(i)
    return indicesInclus

#indicesInclus = indicesEnsemblesInculus(ensembles)

"""rida = imageVide(Simo.shape)

for indice in indicesInclus:
    for couple in ensembles[indice]:
        rida[couple[0],couple[1]] = 0 

afficherImage(rida)"""
        



#print(indicesEnsemblesInculus(ensembles))


def supprimerEnsemblesInclus(ensembles):
    resultat = ensembles.copy()
    indices =   indicesEnsemblesInculus(resultat)   
    for i in range(len(indices) -1,-1,-1):
        indice = indices[i]
        if (indice < len(resultat)):
            resultat.pop(indice)
    return resultat
 


def estAccent(ensemble1 , ensemble2): #ensemble 1 est accent de l'ensemble 2 ?
    Xensemble1 = [ l[0] for l in ensemble1 ]
    Yensemble1 = [ l[1] for l in ensemble1 ]
    XminEnsemble1 = min(Xensemble1)
    XmaxEnsemble1 = max(Xensemble1)
    YminEnsemble1 = min(Yensemble1)
    YmaxEnsemble1 = max(Yensemble1)
    
    Xensemble2 = [ l[0] for l in ensemble2 ]
    Yensemble2 = [ l[1] for l in ensemble2 ]
    XminEnsemble2 = min(Xensemble2)
    XmaxEnsemble2 = max(Xensemble2)
    YminEnsemble2 = min(Yensemble2)
    YmaxEnsemble2 = max(Yensemble2) 
    Ymoyenne1 = int((YminEnsemble1 + YmaxEnsemble1)/2)
    Ymoyenne2 = int((YminEnsemble2 + YmaxEnsemble2)/2)
    if ( XmaxEnsemble1 < XminEnsemble2 and  np.abs(Ymoyenne1 - Ymoyenne2) < 14):
        return True
    return False


#ensembles = supprimerEnsemblesInclus(ensembles)




def fusionnerAccents(ensembles):
    ensembles1 = ensembles.copy()
    nbr = len(ensembles1)
    indicesSupprimer = []
    for i in range(nbr):
            for j in range(nbr):
                #print(estInclu(ensembles[i], ensembles[j]) )
                if (i != j and estAccent(ensembles1[i], ensembles1[j]) ):
                    ensembles1[j] = sorted(ensembles1[j] + ensembles1[i])
                    indicesSupprimer.append(i)
    for i in range(len(indicesSupprimer) -1,-1,-1):
        indice = indicesSupprimer[i]
        ensembles1.pop(indice)
    return ensembles1
                
#ensembles = fusionnerAccents(ensembles)


def organiserLettres(ensembles):
    resultats = []
    liste = []
    i= 0
    for ensemble in ensembles:
        Ymin = min([ l[1] for l in ensemble ])
        liste.append((Ymin, i))
        i = i + 1
    liste = sorted(liste)
    for couple in liste:
        resultats.append(ensembles[couple[1]])
    return resultats




#ensembles = organiserLettres(ensembles)
#print(len(ensembles))

def extremitesContours(ensembles):
    resultats = []
    k = 0
    Xgauche = 1000
    espace = 30
    for ensemble in ensembles:
        resultat = []
        X = [l[0] for l in ensemble]
        Y = [l[1] for l in ensemble]
        i = 0
        while(i < len(X) - 1):
            liste = []
            j = i
            while(j < len(X) and X[i] == X[j]):
                liste.append(Y[j])
                j = j+1
            resultat.append( (X[i] ,   (np.min(liste) - 1 , np.max(liste) + 2)) )
            i = j
        Xmin = np.min(X)
        Xmax = np.max(X)
        Ymin = np.min(Y)
        Ymax = np.max(Y)
        if (k == 0 ):
            resultats.append( [Xmin , Xmax , Ymin, Ymax , resultat ] )
            Ygauche = Ymax
            k=1
        else:
            if ( Ymin - Ygauche > espace ):
                resultats.append("espace")
            resultats.append( [Xmin , Xmax , Ymin, Ymax , resultat ] )
            Ygauche = Ymax
            k=1
    return resultats

#extremites = extremitesContours(ensembles)

#print(len(extremites))

def reconstruireImageLettre(extremites , imgLigne):
    resultats = []
    for extremite in extremites:
        if (extremite == "espace"):
            resultats.append(extremite)
        else:
            [Xmin , Xmax , Ymin, Ymax , extremite1] = extremite
            hauteur = Xmax - Xmin
            largeur = Ymax - Ymin
            largeurMoyenne = (Ymax + Ymin)/2
            distance = max(hauteur , largeur) 
            lettreImage = imageVide((distance + 10, distance + 10))
            for (x , coupleY) in extremite1:
                for y in range( coupleY[0] , coupleY[1] + 1 ):
                    lettreImage[x - Xmin  + int((distance - Xmax + Xmin)/2 + 4)][y - Ymin   + int((distance - Ymax + Ymin)/2) + 4] = imgLigne[x][y]     
            resultats.append(lettreImage)
    return resultats



#mots = reconstruireImageLettre(extremites , LigneT)


#i = 0



Sortie = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def predictionAlphabet(liste):
    indice = np.argmax(liste)
    return Sortie[indice]

#L = [0. , 0. ,  0. ,  0. , 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

#print(predictionAlphabet(L))

"""text_final = ""
for mot in mots:
    if (mot == "espace"):
        text_final = text_final + " "
    else:    
        mot = cv2.resize(mot,(28,28))
        mot = inverseValeursImage(mot)
        afficherImage(mot)
        print(mot.shape)
        #print(cls.predict(np.array([mot]))[0])

            
            

print(text_final)"""



model = load_model('HHORS.h5')


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

images =ligneText(image,step)
for LigneT in images:
    #•LigneT = skimage.filters.gaussian(LigneT,sigma = 0.1)
    afficherImage(LigneT)
    contours = measure.find_contours(LigneT, 0.8)
    ensembles = contourIndiceEntier(contours)
    indicesInclus = indicesEnsemblesInculus(ensembles)
    ensembles = supprimerEnsemblesInclus(ensembles)
    ensembles = fusionnerAccents(ensembles)
    ensembles = organiserLettres(ensembles)
    extremites = extremitesContours(ensembles)
    mots = reconstruireImageLettre(extremites , LigneT)
    text_final = ""
    for mot in mots:
        if (mot == "espace"):
            text_final = text_final + " "
        else:
            #mot = skimage.filters.gaussian(mot,sigma = 0.2)    
            mot = inverseValeursImage(mot)/255
            mot = cv2.resize(mot,(28,28))
            
            #afficherImage(mot)
            alphabet = predictionAlphabet(model.predict(np.array([mot]))[0])
            print(alphabet)
            text_final = text_final + alphabet
    print(text_final)
    