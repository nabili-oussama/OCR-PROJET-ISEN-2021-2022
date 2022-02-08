# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 18:51:14 2022

@author: oussa
"""

from class_Preprocessing import Preprocessing
from class_IHWCGenerator import IHWCGenerator

#Chargement de l'image
IMG8 = Preprocessing('IMG8.jpg')

#Affichage de l'image
IMG8.afficherImage()

#Redimensionnement de l'image
IMG8.redimensionnerImage(1000)

IMG8.afficherImage()

#Nettoyage de l'image
IMG8.nettoyerImage()

IMG8.afficherImage()

#Extraction de lignes de textes 
lignes,imgs = IHWCGenerator.ligneText(IMG8)

i = 0

while i < len(imgs):
    
    imgs[i].afficherImage()
    ensembles = IHWCGenerator.contourIndiceEntier(imgs[i])
    
    resultat = IHWCGenerator.supprimerEnsemblesInclus(ensembles)
    
    resultat = IHWCGenerator.fusionnerAccents(resultat)
    
    resultat = IHWCGenerator.organiserLettres(resultat)
    
    resultat = IHWCGenerator.reconstruireImageLettre(resultat, imgs[i], lignes[i])
    
    for j in resultat :
        if type(j) == str:
            print("espace")
        else :    
            j.afficherImage()
    i+=1
        
    
    
    
