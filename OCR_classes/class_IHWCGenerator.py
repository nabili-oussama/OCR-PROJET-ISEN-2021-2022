# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:14:53 2022
@author: oussama nabili - reda zerrari - harith jadid
"""
from class_Preprocessing import Preprocessing

import numpy as np

from skimage import measure

class IHWCGenerator :

    def lineText(image):
        """
        Allows you to locate the coordinates that delimit each line of text 
	and ignore empty lines and finally generate their image.
        
        Parameters:
        image : image file (loaded from the loadImage function)
    
        Returns:
        Returns a list containing the coordinates as a start and end tuple 
	and another list containing the image of each line of text.
        
        
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
            
        liste = []  
        for (x,y) in images:
            liste.append(Preprocessing(image.image[x:y,:]))
            
        return images,liste
    
    def contourIndexInteger(image):
        """
        Generates a list of lists of reals each containing the coordinates of the contours of each character,
	then converts these reals into integers and sorts them in ascending order then removes duplicates.
        
        Parameters:
        image : image file (loaded from the loadImage function)
    
        Returns:
        Returns a list of lists containing the outline coordinates (inner and outer) of each character
        
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

    def isIncluded(set1 , set2):
        """
        Checks if the set1 outline is included in the set2 outline by comparing their endpoints.
        
        Parameters:
        	set1 : liste des coordonnées d'un contour
		set2 : liste des coordonnées d'un contour
    
        Returns:
        Returns True if set1 is included in set2, False otherwise
        
        """
        
        Xensemble1 = [ l[0] for l in set1 ]
        Yensemble1 = [ l[1] for l in set1 ]
        XminEnsemble1 = min(Xensemble1)
        XmaxEnsemble1 = max(Xensemble1)
        YminEnsemble1 = min(Yensemble1)
        YmaxEnsemble1 = max(Yensemble1)
        
        Xensemble2 = [ l[0] for l in set2 ]
        Yensemble2 = [ l[1] for l in set2 ]
        XminEnsemble2 = min(Xensemble2)
        XmaxEnsemble2 = max(Xensemble2)
        YminEnsemble2 = min(Yensemble2)
        YmaxEnsemble2 = max(Yensemble2)
		   
        if (XminEnsemble1 > XminEnsemble2 and YminEnsemble1 > YminEnsemble2 and \
	    XmaxEnsemble1 < XmaxEnsemble2 and YmaxEnsemble1 < YmaxEnsemble2):
            return True
        return False

    def indexSetIncluded(ensembles):
        """
        Calls the isIncluded function to check if an outline is an interior outline and stores its index in a new list.
         
        Parameters:
        ensembles (ndarray) : list of lists containing the coordinates of the contours (interior and exterior)
			      of each character.
    
        Returns:
        Returns a list containing the indices of the interior contours in the list 'ensembles'
        
        """
        nbr = len(ensembles)
        indicesInclus = []
        for i in range(nbr):
            for j in range(nbr):
                if (i != j and IHWCGenerator.isIncluded(ensembles[i], ensembles[j]) ):
                    indicesInclus.append(i)
        return indicesInclus
    
    def removeIncludedSets(ensembles):
        """
        Calls the indexSetIncluded function to remove lists from interior boundaries.
         
        Parameters:
        ensembles (ndarray) : list of lists containing the coordinates of the contours 
			      (interior and exterior) of each character
    
        Returns:
	Returns a list of lists containing the coordinates of the outer contours only.      
	
        """
        resultat = ensembles.copy()
        indices = IHWCGenerator.indexSetIncluded(resultat)   
        for i in range(len(indices) -1,-1,-1):
            indice = indices[i]
            resultat.pop(indice)
        return resultat
    
    def isAccent(set1 , set2):
        """
        Checks if 'set1' is accent of 'set2' based on their positions;
        the min and max of the coordinates along the OX axis and along the OY axis are taken;
        we compare the coordinates of the two positions and if we verify the following two conditions:
                - 'set2' is below 'set1'.
                - 'set2' is not too far from 'set1' along the OY axis.  
        
        then 'set1' is accent of 'set2'.
            
        Parameters:
        set1 (list(int)): list containing the coordinates of the contour of 'set1'
        set2 (list(int)): list containing the coordinates of the contour of 'set2'
            
        Returns:
        (bool) Returns True if 'set1' is accent of 'set2' and returns False otherwise.
        """
        Xensemble1 = [ l[0] for l in set1 ]
        Yensemble1 = [ l[1] for l in set1 ]
        #XminEnsemble1 = min(Xensemble1)
        XmaxEnsemble1 = max(Xensemble1)
        YminEnsemble1 = min(Yensemble1)
        YmaxEnsemble1 = max(Yensemble1)
        
        Xensemble2 = [ l[0] for l in set2 ]
        Yensemble2 = [ l[1] for l in set2 ]
        XminEnsemble2 = min(Xensemble2)
        #XmaxEnsemble2 = max(Xensemble2)
        YminEnsemble2 = min(Yensemble2)
        YmaxEnsemble2 = max(Yensemble2) 
        Ymoyenne1 = int((YminEnsemble1 + YmaxEnsemble1)/2)
        Ymoyenne2 = int((YminEnsemble2 + YmaxEnsemble2)/2)
        if ( XmaxEnsemble1 < XminEnsemble2 and  np.abs(Ymoyenne1 - Ymoyenne2) < 14):
            return True
        return False
    
    def mergeAccents(sets):
        """
        Merges the accent with the character it belongs to.
        it is given the list 'sets' containing lists of coordinates of all contours.
        it goes through the whole list and calls the isAccent() function to check if there are accents.
    
        if it is found that there is an accent associated with an element; we merge the two lists
	(the list containing the character coordinates and the list containing the accent coordinates).
    
        the coordinates of the accents are removed from the list.
        
        Parameters:
        sets (list): list of lists containing the coordinates of the outlines of the elements.
   
        
        Returns:
        (list) Returns a list of lists containing the coordinates of the outlines 
	       (in addition to the merged elements with their accents).
        """
        sets1 = sets.copy()
        nbr = len(sets1)
        indicesSupprimer = []
        for i in range(nbr):
                for j in range(nbr):
                    #print(estInclu(sets[i], sets[j]) )
                    if (i != j and IHWCGenerator.isAccent(sets1[i], sets1[j]) ):
                        sets1[j] = sorted(sets1[j] + sets1[i])
                        indicesSupprimer.append(i)
        for i in range(len(indicesSupprimer) -1,-1,-1):
            indice = indicesSupprimer[i]
            sets1.pop(indice)
        return sets1
    
    def arrangeLetters(ensembles):
        """
        Reorganise la liste contennant les listes de contours des lettres en fonctions
        de leurs positions selon l'axe OY dans un ordre croissant.
        
        Parameters:
        ensembles (list): list of lists containing the coordinates of the contours of the letters.
   
    
        Returns:
        (list) returns a list of lists containing the coordinates of ordered letters.
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
    
    def extremitiesContours(ensembles):
        """
        This method makes it possible to delimit the contours,
        i.e. to find the Max and the min along the two axes OX and OY,
        in addition to finding the next local Max and Min OY for each X.
        
        Parameters:
        ensembles (list): list of lists containing the coordinates of the contours of the letters.
            
        returns:
        (list) returns a list of lists containing the ends of each character (letter).
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
                    resultats.append("space")
                resultats.append( [Xmin , Xmax , Ymin, Ymax , resultat ] )
                lastYmax = Ymax

        return resultats
         
""" not done ||
	     \/  """
	
    def rebuildImageLetter(ensembles , imgLigne, Ligne):
        """
        Permet de générer une image pour chaque caractère présent dans la ligne passée en paramètre 
        
        Parameters:
        ensembles (list)         : liste de listes contenant les coordonnées des contours des lettres.
        imgLigne (class_Preprocessing.Preprocessing): l'image qui représente la ligne
        Ligne (tuple(int,int)): un tuple contenant le début et la fin de la ligne
        
        returns:
        (list) une liste contenant les images de chaque caractère présent dans la ligne 
        
        """
        
        extremites = IHWCGenerator.extremitiesContours(ensembles)
        
        resultats = []
        
        for extremite in extremites:
            if (extremite == "space"):
                resultats.append(extremite)
            else:
                [Xmin , Xmax , Ymin, Ymax , extremite1] = extremite
                hauteur = Ligne[1] - Ligne[0]
                largeur = Ymax - Ymin
                distance = max(hauteur , largeur) 
                lettreImage = Preprocessing.emptyImage((distance , distance))
                for (x , coupleY) in extremite1:
                    for y in range( coupleY[0] , coupleY[1] + 1 ):
                        lettreImage.image[x][y - Ymin + int((hauteur - Ymax + Ymin)/2)] = imgLigne.image[x][y]     
                resultats.append(lettreImage)
        return resultats