# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:06:54 2023

@author: excalibur
"""
from PyQt5 import uic
 
with open('veri.py','w', encoding = 'utf-8') as fout:
    uic.compileUi('rezervasyon.ui',fout)