# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 18:51:14 2022

@author: oussa
"""
import numpy as np 
import string
import tensorflow as tf
from tensorflow import keras
import cv2

def predictModel2(image, h5path):
    
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    model = tf.keras.models.load_model(h5path)    
    probs = model.predict(image)
    print(probs)
    prediction = probs.argmax(axis=1)
    label = labels[prediction[0]]
    
    return label

def inverseValeursImage(image):
    resultat = image.copy()
    for i in range(resultat.shape[0]):
        for j in range(resultat.shape[1]):
            if resultat[i][j] == 0:
                resultat[i][j] = 255
            else:
                resultat[i][j] = 0
    return resultat

def predictModel1(image, h5path):
    
    
    numbers = [str(i) for i in range(0,10)]
    labels = list(numbers + list(string.ascii_letters) )
    
    model = tf.keras.models.load_model(h5path)    
    probs = model.predict(image)
    prediction = probs.argmax(axis=1)
    label = labels[prediction[0]]
    
    return label

def predictionAlphabet(liste):
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    indice = np.argmax(liste)
    return labels[indice]

from class_Preprocessing import Preprocessing
from class_IHWCGenerator import IHWCGenerator

if __name__ == '__main__':
    #Chargement de l'image
    IMG8 = Preprocessing('p1.jpg')

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

    model = tf.keras.models.load_model("my_model.h5")

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    i = 0
    p=0
    while i < len(imgs):

        imgs[i].afficherImage()
        cv2.imwrite("genimages/lignep1{0}.jpg".format(i+1), imgs[i].image)
        
        ensembles = IHWCGenerator.contourIndiceEntier(imgs[i])
        
        resultat = IHWCGenerator.supprimerEnsemblesInclus(ensembles)
        
        resultat = IHWCGenerator.fusionnerAccents(resultat)
        
        resultat = IHWCGenerator.organiserLettres(resultat)
        
        resultat = IHWCGenerator.reconstruireImageLettre(resultat, imgs[i], lignes[i])
        text_final = ""
        for j in resultat :   
            if type(j) == str:
                print("espace")
                text_final = text_final + " "
            else :    
                j.afficherImage()
                cv2.imwrite("genimages/p1{0}.jpg".format(p+1), j.image)
                mot = inverseValeursImage(j.image)/255
                mot = cv2.resize(mot,(32,32))
                
                #afficherImage(mot)
                alphabet = predictionAlphabet(model.predict(np.array([mot]))[0])
                #print(alphabet)
                text_final = text_final + alphabet
                
            p+=1

        i+=1
            
print(text_final)    




        
        
