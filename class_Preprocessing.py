# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:14:53 2022
@author: oussa
"""

import cv2
from skimage.filters import threshold_sauvola
from skimage import img_as_ubyte


class Preprocessing :
    

    def __init__(self,image):
        
        if type(image)==str:
            self.image  = Preprocessing.chargerImage(image,0)
        else:
            self.image = image  
            
        self.dimX = self.image.shape[0]
        self.dimY = self.image.shape[1]
    
    def chargerImage(image, Type = 1):

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
        return cv2.imread(image,Type)
    
    def afficherImage(self):
        
        """
        Lance et ferme la fenêtre de l'image.
    
        Parameters:
        image : fichier image (charger depuis la fonction chargerImage)
    
        Returns:
        Aucun retour
        
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
        Aucun retour
        
        
        """

        self.dimX = self.dimX * largeur//self.dimY
        self.dimY = largeur
        
        self.image = cv2.resize(self.image,(self.dimY,self.dimX))
        
    
    def nettoyerImage(self):
        """
        Permet de nettoyer l'image.
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
        Aucun retour
        
        """
        thresh_sauvola = threshold_sauvola(self.image)
        binary_sauvola = self.image > thresh_sauvola
        binary_sauvola = img_as_ubyte(binary_sauvola)
        
        self.image = binary_sauvola
    
    def imageVide(dim):
        """
        Une méthode qui permet de creer une image vide.
        Matrice de 255.
        
        Parameters:
        dim (int,int) : tuple qui represente les dimensions (x,y)
        
        returns: 
        (class_Preprocessing.Preprocessing) image vide.
        """
        return Preprocessing(img_as_ubyte([[255 for i in range(dim[1])] for j in range(dim[0])]))
