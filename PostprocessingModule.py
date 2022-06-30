# -*- coding: utf-8 -*-
"""
@author: oussama - reda - harith
"""

import string
from spellchecker import SpellChecker

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
