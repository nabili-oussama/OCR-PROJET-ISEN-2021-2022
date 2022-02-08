# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:14:53 2022
@author: oussa
"""
from class_Preprocessing import Preprocessing

import numpy as np

from skimage import measure

class IHWCGenerator :

    def ligneText(image):
        """
        Permet de localiser les coordonnées qui délimitent chaque ligne 
	    de texte et ignore les lignes vides.
        
        Parameters:
        image : fichier image (charger depuis la fonction chargerImage)
    
        Returns:
        Retourne une liste contenant les coordonnées sous forme de tuple de début et de fin 
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
    
            liste.append((min(debutG, debutD) , max(finG, finD) ))
            
        i = 0
        while(i < len(liste)-1):
            (d1 , f1) = liste[i]
            (d2 , f2) = liste[i+1]
            if (f1 < d2 and f1 < image.dimX and d2 < image.dimX and np.mean(image.image[f1:d2,:]) < 254):
                images.append( ( f1 , d2 ) )
            i = i+1
            
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
                if (i != j and IHWCGenerator.estInclu(ensembles[i], ensembles[j]) ):
                    indicesInclus.append(i)
        return indicesInclus
    
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
        indices = IHWCGenerator.indicesEnsemblesInclus(resultat)   
        for i in range(len(indices) -1,-1,-1):
            indice = indices[i]
            resultat.pop(indice)
        return resultat
    
    def estAccent(ensemble1 , ensemble2):
        """
        Vérifie si l''ensemble1' est accent de l''ensemble2' en fonction de leurs positions;
        on prend le min et le max des coordonnées suivant l'axe OX et suivant l'axe OY;
        on compare les coordonnées des deux positions et si on vérifie les deux conditions suivantes :
                - l''ensemble2'est au-dessous de l''ensemble1'.
                - l''ensemble2' n'est pas trop loin de l''ensemble1' suivant l'axe OY.    
        
        alors l''ensemble1' est accent de l''ensemble2'.
            
        Parameters:
        ensemble1 (liste(int)): liste contenant les coordonnées du contour de 'ensemble1'
        ensemble2 (liste(int)): liste contenant les coordonnées du contour de 'ensemble2'
            
        Returns:
        (bool) retourne True si l''ensemble1' est accent de l''ensemble2' et retourne False sinon.

        """
        Xensemble1 = [ l[0] for l in ensemble1 ]
        Yensemble1 = [ l[1] for l in ensemble1 ]
        #XminEnsemble1 = min(Xensemble1)
        XmaxEnsemble1 = max(Xensemble1)
        YminEnsemble1 = min(Yensemble1)
        YmaxEnsemble1 = max(Yensemble1)
        
        Xensemble2 = [ l[0] for l in ensemble2 ]
        Yensemble2 = [ l[1] for l in ensemble2 ]
        XminEnsemble2 = min(Xensemble2)
        #XmaxEnsemble2 = max(Xensemble2)
        YminEnsemble2 = min(Yensemble2)
        YmaxEnsemble2 = max(Yensemble2) 
        Ymoyenne1 = int((YminEnsemble1 + YmaxEnsemble1)/2)
        Ymoyenne2 = int((YminEnsemble2 + YmaxEnsemble2)/2)
        if ( XmaxEnsemble1 < XminEnsemble2 and  np.abs(Ymoyenne1 - Ymoyenne2) < 14):
            return True
        return False
    
    def fusionnerAccents(ensembles):
        """
        Fusionne l'accent avec le caractère auquel elle appartient.
        on lui donnant la liste 'ensembles'  contenant des listes de coordonnées de tous les contours.
        elle parcourt toute la liste et elle fait appel à la fonction estAccent() pour vérifier s'il y a des
        accents.
    
        si on trouve qu'il y a un accent associé à un élément; on fusionne les deux listes
        (la liste contenant les coordonnées de caractère et la liste contenant les coordonnées de l'accent).
    
        on supprime les coordonnées des accents de la liste.
        
        Parameters:
        ensembles (list): liste de listes contenant les coordonnées des contours des éléments.
   
        
        Returns:
        (liste) retourne une liste de listes contenant les coordonnées des contours (en plus des éléments 
        fusionnés avec leurs accents).
        """
        ensembles1 = ensembles.copy()
        nbr = len(ensembles1)
        indicesSupprimer = []
        for i in range(nbr):
                for j in range(nbr):
                    #print(estInclu(ensembles[i], ensembles[j]) )
                    if (i != j and IHWCGenerator.estAccent(ensembles1[i], ensembles1[j]) ):
                        ensembles1[j] = sorted(ensembles1[j] + ensembles1[i])
                        indicesSupprimer.append(i)
        for i in range(len(indicesSupprimer) -1,-1,-1):
            indice = indicesSupprimer[i]
            ensembles1.pop(indice)
        return ensembles1
    
    def organiserLettres(ensembles):
        """
        Reorganise la liste contennant les listes de contours des lettres en fonctions
        de leurs positions selon l'axe OY dans un ordre croissant.
        
        Parameters:
        ensembles (list): liste de listes contenant les coordonnées des contours des lettres.
   
    
        Returns:
        (list) retourne une liste de listes contenant les coordonnées des lettres ordonnées.
        """
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
        """
        Cette méthode permet de délimiter les contours,
        c'est à dire de trouver le Max et le min suivant les deux axes OX et OY,
        en plus de trouver le Max et le min local suivant OY pour chaque X.
        
        Parameters:
        ensembles (list): liste de listes contenant les coordonnées des contours des lettres.
            
        returns:
        (list) retourne une liste de listes contenants les extrémités de chaque caractère (lettre).
        ===> [...,[Xmin, Xmax, Ymin, Ymax, [...,(X[i],(YX[i]max ,YX[i]min)),...]],...]
        
        """
        resultats = []
        k = 0
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
                    j = j + 1
                resultat.append( (X[i] ,   (np.min(liste) , np.max(liste))) )
                i = j
            Xmin = np.min(X)
            Xmax = np.max(X)
            Ymin = np.min(Y)
            Ymax = np.max(Y)
            if (k == 0 ):
                resultats.append( [Xmin , Xmax , Ymin, Ymax , resultat ] )
                lastYmax = Ymax
                k = 1
            else:
                if ( Ymin - lastYmax > espace ):
                    resultats.append("espace")
                resultats.append( [Xmin , Xmax , Ymin, Ymax , resultat ] )
                lastYmax = Ymax

        return resultats
            
    def reconstruireImageLettre(ensembles , imgLigne):
        """
        Permet de générer une image pour chaque caractère présent dans la ligne passée en paramètre 
        
        Parameters:
        ensembles (list)         : liste de listes contenant les coordonnées des contours des lettres.
        imgLigne (tuple(int,int)): un tuple contenant le début et la fin d'une ligne
        
        returns:
        (list) une liste contenant les images de chaque caractère présent dans la ligne 
        
        """
        
        extremites = IHWCGenerator.extremitesContours(ensembles)
        
        resultats = []
        
        for extremite in extremites:
            if (extremite == "espace"):
                resultats.append(extremite)
            else:
                [Xmin , Xmax , Ymin, Ymax , extremite1] = extremite
                hauteur = imgLigne[1] - imgLigne[0]
                largeur = Ymax - Ymin
                distance = max(hauteur , largeur) 
                lettreImage = Preprocessing.imageVide((distance , distance))
                for (x , coupleY) in extremite1:
                    for y in range( coupleY[0] , coupleY[1] + 1 ):
                        lettreImage.image[x][y - Ymin + int((hauteur - Ymax + Ymin)/2)] = imgLigne[x][y]     
                resultats.append(lettreImage.image)
        return resultats
