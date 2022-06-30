# -*- coding: utf-8 -*-
"""
@author: oussama - reda - harith
"""
import numpy as np 
import string

import tensorflow as tf
from tensorflow import keras

import cv2

from class_Preprocessing import Preprocessing
from class_IHWCGenerator import IHWCGenerator

from spellchecker import SpellChecker

#from PostprocessingModule.py import AlphVsNum, CorrectionDigits, spellChecking

def predictModel2(image, h5path):
    
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    model = tf.keras.models.load_model(h5path)    
    probs = model.predict(image)
    print(probs)
    prediction = probs.argmax(axis=1)
    label = labels[prediction[0]]
    
    return label

def inverseImageValues(image):
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

def AlphVsNum(mot):
    c = 0
    mot = list(mot)
    for i in mot:
        if i in list(string.ascii_uppercase + string.ascii_lowercase):
            c + = 1
    return c/(len(mot))
        

def CorrectionDigits(mot):
    if AlphVsNum(mot) >= 0.5:
        mot = list(mot)
        for i in range(len(mot)):
            if mot[i] == '0':
                mot[i] = "O"
            if mot[i] == '5':
                mot[i] = "S"
            if mot[i] == '9':
                mot[i] = "q"
            if mot[i] == '8':
                mot[i] = "j"
    return "".join(mot)

def spellChecking(txt):
    
    spell = SpellChecker()

    corrected_text = ''

    # find those words that may be misspelled
    misspelled = spell.unknown(text.split())

    for word in misspelled:
        # Get the one `most likely` answer
        corrected_text = corrected_text + spell.correction(word)

if __name__ == '__main__':
    #Chargement de l'image
    IMG8 = Preprocessing('IMG8.jpg') # assurez-vous que l'image est dans le même dossier avec le fichier .py

    #Affichage de l'image
    IMG8.showImage()

    #Redimensionnement de l'image
    IMG8.resizeImage(1000)

    IMG8.showImage()

    #Nettoyage de l'image
    IMG8.cleanImage()

    IMG8.showImage()

    #Extraction de lignes de textes 
    lignes,imgs = IHWCGenerator.lineText(IMG8)

    model = tf.keras.models.load_model("my_model.h5")

    model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])
    
    i = 0
    p = 0
    
    while i < len(imgs):

        imgs[i].showImage()
        cv2.imwrite("genimages/lignep1{0}.jpg".format(i+1), imgs[i].image)
        
        ensembles = IHWCGenerator.contourIndexInteger(imgs[i])
        
        resultat = IHWCGenerator.removeIncludedSets(ensembles)
        
        resultat = IHWCGenerator.mergeAccents(resultat)
        
        resultat = IHWCGenerator.arrangeLetters(resultat)
        
        resultat = IHWCGenerator.rebuildImageLetter(resultat, imgs[i], lignes[i])
        
        text_final = ""
        
        for j in resultat :   
            if type(j) == str:
                #print("space")
                text_final = text_final + " "
            else :    
                j.showImage()
                cv2.imwrite("genimages/p1{0}.jpg".format(p+1), j.image)
                mot = inverseImageValues(j.image)/255
                mot = cv2.resize(mot,(32,32))
                
                #showImage(mot)
                alphabet = predictionAlphabet(model.predict(np.array([mot]))[0])
                #print(alphabet)
                text_final = text_final + alphabet
                
            p+=1
        i+=1
        
txt = ""
for word in final_text.split():
    txt = txt + CorrectionDigits(word) + " "
    
txt = spellChecking(txt)

print(txt)    




        
        
