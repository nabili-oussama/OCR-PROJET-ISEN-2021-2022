# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:14:53 2022

@author: jad
"""

import cv2
import numpy as np
from skimage.filters import (threshold_otsu, threshold_triangle,
threshold_niblack, threshold_sauvola)
from skimage import img_as_ubyte


import matplotlib.pyplot as plt

from skimage import measure

class Preprocessing :
    
    def __init__(self,image):
        
        self.image  = chargerImage(image)
        (self.dimX,self.dimY) = self.image.shape
        #self.dimX = self.image.shape[0]
        #self.dimY = self.image.shape[1]
    
    def chargerImage(self, Type = 1):

        """"
        La méthode charge une image à partir du fichier spécifié.
        Si l'image ne peut pas être lue (à cause d'un fichier manquant,
        d'autorisations incorrectes, d'un format non pris en charge ou invalide),
        cette méthode renvoie une matrice vide.
        
        Parameters:
        lien (string): le chemin vers le fichier image
        Type (int)   : il spécifie la manière dont l'image doit être lue.
                       Sa valeur par défaut est 1 (Toute transparence d'image sera négligée)
                       Si Type = 0 charger l'image en mode niveaux de gris
    
        Returns:
        Cette méthode renvoie une image qui est chargée à partir du fichier spécifié
        
        """
        return cv2.imread(self.image,Type)
    
    
    
    def afficherImage(self):
        
        """
        Une methode utilisé pour afficher une image dans une fenêtre.
        La fenêtre s'adapte automatiquement à la taille de l'image.
        
        
        Parameters:
        image : fichier image (charger depuis la fonction chargerImage)
    
        Returns:
        pas de retour
        
        """
        cv2.imshow("Fenetre",self.image)  
        cv2.waitKey(0)
        # cv2.waitKey(2000)
        cv2.destroyAllWindows()
    
    def redimensionnerImage(self,largeur):
        """
        Permet de redimensionner une image en gardant les mêmes proportions.
        
        
        Parameters:
        image         : fichier image (charger depuis la fonction chargerImage)
        largeur (int) : la largeur utiliser pour redimensionner
    
        Returns:
        Cette méthode renvoie une image redimensionner
        
        
        """

        self.dimX = self.dimX * largeur//self.dimY
        self.dimY = largeur
        return cv2.resize(self.image,(self.dimY,self.dimX))
    
    def nettoyerImage(self):
        """
        Applique le seuil local de Sauvola à un tableau. Sauvola est une
        modification de la technique Niblack.
        
        Dans la méthode originale, un seuil T est calculé pour chaque pixel
        dans l'image en utilisant la formule suivante :
        
            T = m(x,y) * (1 + k * ((s(x,y) / R) - 1))
        
        où m(x,y) et s(x,y) sont la moyenne et l'écart type de
        voisinage de pixel (x,y) défini par une fenêtre rectangulaire de taille w
        fois w centré autour du pixel. k est un paramètre configurable
        qui pondère l'effet de l'écart type.
        R est l'écart type maximal d'une image en niveaux de gris.
        
        Parameters:
        image : fichier image (charger depuis la fonction chargerImage)
    
        Returns: (ndarray)
        Cette méthode renvoie une image nettoyer 
        
        """
        thresh_sauvola = threshold_sauvola(self.image)
        binary_sauvola = self.image > thresh_sauvola
        binary_sauvola = img_as_ubyte(binary_sauvola)
        return binary_sauvola



class IHWCGenerator :
    
    def imageVide(dim):
        """
        Permet de générer une image vide dont les dimensions sont passées en paramètre
        Matrice de 255
        
        Parameters:
        dim (int,int) : tuple qui contient les dimensions de l'image à générer
    
        Returns:
        Retourne une image vide (ndarray)
        
        """
        return Preprocessing(img_as_ubyte([[255 for i in range(dim[1])] for j in range(dim[0])]))
    
    
    def ligneText(image):
        """
        Permet de localiser les coordonnées qui délimitent chaque ligne 
	    de texte et ignore les lignes vides.
        
        Parameters:
        image : fichier image (charger depuis la fonction chargerImage)
    
        Returns:
        Retourne une liste contenant les coordonnées de début et de fin 
        de chaque ligne de texte
        
        """
        liste = []
        images = []
        
        i = 0
        j = 0
        while(i < image.dimX):
            while(i < image.dimX and image.image[i,5] == 255):
                i = i + 1
            debutG = i
            while(j < image.dimX and image.image[j,image.dimY-5] == 255):
                j = j + 1
            debutD = j        
            while(i < image.dimX and image.image[i,5] == 0):
                i = i+1
            finG = i
            while(j < image.dimX and image.image[j,image.dimY-5] == 0):
                j = j+1
            finD = j
    
            
            #print(debutG, debutD , finG, finD)
            
            liste.append((min(debutG, debutD) , max(finG, finD) ))
        #print(liste)    
        i = 0
        while(i < len(liste)-1):
            (d1 , f1) = liste[i]
            (d2 , f2) = liste[i+1]
            if (f1 < d2 and f1 < image.dimX and d2 < image.dimX and np.mean(image.image[f1:d2,:]) < 254):
                images.append( ( f1 , d2 ) )
            i = i+1
        #print(liste)
        
        #i = 0
        #while(i < len(cordonnees)):
         #   (d,f) = cordonnees[i]
          #  if():
           #     images.append( image[d:f,:])
		            #i= i + 1
        return images
    
    
    
    def contourIndiceEntier(image):
        """
        Génére une liste de listes de réels contenant chaqune les coordonnées des contours de chaque 
		caractère, puis convertit ces réels en entiers et les trie en ordre croissant puis supprime 
	    les doublons.
        
        Parameters:
        image : fichier image (charger depuis la fonction chargerImage)
    
        Returns:
        Retourne une liste de listes contenant les coordonnées des contours (intérieur et extérieur) 
	    de chaque caractère
        
        """
	    contours = measure.find_contours(image.image, 0.8)
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
    
    def estInclu(ensemble1 , ensemble2):
        """
        Vérifie si le contour ensemble1 est inclu dans le contour ensemble2 
	    en comparant leurs extrémités.
        
        Parameters:
        ensemble1 : liste des coordonnées d'un contour
		ensemble2 : liste des coordonnées d'un contour
    
        Returns:
        Retourne True si ensemble1 est inclu dans ensemble2, 
        False sinon
        
        """
        
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
    
    def indicesEnsemblesInclus(ensembles):
		"""
        Fait appel à la fonction estInclu pour vérifier si un contour est un contour intérieur et stock son
		indice dans une nouvelle liste.
         
        Parameters:
        ensembles (ndarray) : liste de listes contenant les coordonnées des contours (intérieur et extérieur) 
	    de chaque caractère
    
        Returns:
        Retourne une liste contenant les indices des contours intérieurs dans la liste 'ensembles'
        
        """
        nbr = len(ensembles)
        indicesInclus = []
        for i in range(nbr):
            for j in range(nbr):
                #print(estInclu(ensembles[i], ensembles[j]) )
                if (i != j and estInclu(ensembles[i], ensembles[j]) ):
                    indicesInclus.append(i)
        return indicesInclus
    
indicesInclus = indicesEnsemblesInclus(ensembles)
    
    """rida = imageVide(Simo.shape)
    
    for indice in indicesInclus:
        for couple in ensembles[indice]:
            rida[couple[0],couple[1]] = 0 
    
    afficherImage(rida)"""
            
    
    
    
    #print(indicesEnsemblesInculus(ensembles))
    
    
    def supprimerEnsemblesInclus(ensembles):
		"""
        Fait appel à la fonction indicesEnsemblesInclus pour supprimer les listes des contours intérieurs.
         
        Parameters:
        ensembles (ndarray) : liste de listes contenant les coordonnées des contours (intérieur et extérieur) 
	    de chaque caractère
    
        Returns:
        Retourne une liste de listes contenant les coordonnées des contours extérieurs uniquement.
        
        """
        resultat = ensembles.copy()
        indices =   indicesEnsemblesInclus(resultat)   
        for i in range(len(indices) -1,-1,-1):
            indice = indices[i]
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
    
    
    def extremitesContours(ensembles):
        resultats = []
        k = 0
        Xgauche = 1000
        espace = 20
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
                resultat.append( (X[i] ,   (np.min(liste) , np.max(liste))) )
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
    
    extremites = extremitesContours(ensembles)
    
    print(len(extremites))
    
    
    
    def reconstruireImageLettre(extremites , imgLigne):
        resultats = []
        for extremite in extremites:
            if (extremite == "espace"):
                resultats.append(extremite)
            else:
                [Xmin , Xmax , Ymin, Ymax , extremite1] = extremite
                hauteur = imgLigne.shape[0]
                largeur = Ymax - Ymin
                largeurMoyenne = (Ymax + Ymin)/2
                distance = max(hauteur , largeur) 
                lettreImage = imageVide((distance , distance))
                for (x , coupleY) in extremite1:
                    for y in range( coupleY[0] , coupleY[1] + 1 ):
                        lettreImage[x][y - Ymin + int((hauteur - Ymax + Ymin)/2)] = imgLigne[x][y]     
                resultats.append(lettreImage)
        return resultats


mots = reconstruireImageLettre(extremites , Simo)

print(len(mots))

for mot in mots:
    if (mot == "espace"):
        print("espace")
    else:
        afficherImage(mot)

 
#imgVide = redimensionnerImage(imgVide, 1000)




"""for couple in ensembles[32]:
        imgVide[couple[0] , couple[1]] = 0
afficherImage(imgVide)"""