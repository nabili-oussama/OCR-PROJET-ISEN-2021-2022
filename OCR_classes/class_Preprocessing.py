# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 11:14:53 2022
@author: oussama nabili - zerrari reda - harith jadid
"""

import cv2
from skimage.filters import threshold_sauvola
from skimage import img_as_ubyte


class Preprocessing:

    def __init__(self, image):
        """
        Build preprocessor from image
        ---
        params:
            image : string (link or path) or ndarray (l image file)
        ---
        constructor
        """
        if type(image) == str:
            self.image = Preprocessing.loadImage(image, 0)
        else:
            self.image = image

        self.dimX = self.image.shape[0]
        self.dimY = self.image.shape[1]

    def loadImage(image, Type=1):

        """"
        The method loads an image from the specified file.
        If the image cannot be read (due to missing file, incorrect permissions,
        unsupported or invalid format), this method returns an empty array.
        
        Parameters:
        image (string): the path to the image file
        Type (int)   : It specifies how the image should be read.
                       Its default value is 1 (Any image transparency will be ignored). 
                       If Type = 0 load the image in grayscale mode.
    
        Returns:
        ndarray - the image loaded after transformation
        
        """
        return cv2.imread(image, Type)

    def showImage(self):

        """
        Launches and closes the image window.
   
        Parameters:
        image : fichier image (charger depuis la fonction loadImage)
    
        Returns:
        No return
        
        """
        cv2.imshow("Window", self.image)
        cv2.waitKey(0)
        # cv2.waitKey(2000)
        cv2.destroyAllWindows()

    def resizeImage(self, lenght):
        """
        Allows you to resize an image while keeping the same proportions.
        
        
        Parameters:
            image        : image file (loaded from the loadImage function)
            lenght (int) : the width to use to resize
    
        Returns:
        No return 
        
        """

        self.dimX = self.dimX * lenght // self.dimY
        self.dimY = lenght

        self.image = cv2.resize(self.image, (self.dimY, self.dimX))

    def cleanImage(self):
        """
        Allows you to clean up the image. 
        Applies the local Sauvola threshold to an array.
        Sauvola is a modification of the Niblack technique. 
        
        In the original method, a threshold T is calculated
        for each pixel in the image using the following formula:
        
            T = m(x,y) * (1 + k * ((s(x,y) / R) - 1))
        
        where m(x,y) and s(x,y) are the mean and standard deviation
        of pixel neighborhood (x,y) defined by a rectangular window 
        of size w times w centered around the pixel. k is a configurable 
        parameter that weights the effect of standard deviation. 
        R is the maximum standard deviation of a grayscale image.
        
        Parameters:
        image : image file (loaded from the loadImage function)
    
        Returns: (ndarray)
        No return 
        
        """
        thresh_sauvola = threshold_sauvola(self.image)
        binary_sauvola = self.image > thresh_sauvola
        binary_sauvola = img_as_ubyte(binary_sauvola)

        self.image = binary_sauvola

    def emptyImage(dim):
        """
        A method to create an empty image. 
        Matrix of 255.
        
        Parameters:
        dim (int,int) : tuple that represents the dimensions (x,y)
        
        returns: 
        (class_Preprocessing.Preprocessing) empty image.
        """
        return Preprocessing(img_as_ubyte([[255 for i in range(dim[1])] for j in range(dim[0])]))
