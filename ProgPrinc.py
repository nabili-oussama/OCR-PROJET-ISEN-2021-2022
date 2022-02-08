# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 18:51:14 2022

@author: oussa
"""

from class_Preprocessing import Preprocessing
from class_IHWCGenerator import IHWCGenerator

IMG8 = Preprocessing('IMG8.jpg')

IMG8.afficherImage()

IMG8.redimensionnerImage(1000)

IMG8.afficherImage()
