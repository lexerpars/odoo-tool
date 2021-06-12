# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 03:26:42 2021

@author: usuario
"""

import pandas as pd

class Excel:
    
    def __init__(self):
        print('inicializando excel')
        pass
    
    def read_file(self,file):
        print('corriendo')
        if file:
            excel = pd.read_excel(file)
            codigo = excel['Codigo'].tolist()
            debit = excel['Debit'].tolist()
            credit = excel['Credit'].tolist()
            formula = excel['Formula'].tolist()
            result = []
            for c in codigo:
                result.append([c,debit[codigo.index(c)],credit[codigo.index(c)],formula[codigo.index(c)]])
            return result
        