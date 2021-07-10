# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 10:14:30 2021

@author: Rogelio
"""

import pyodbc

class intelisis(object):
    
    def __init__(self):
        self.cursor = self.conexion()
        
    
    def conexion(self):
        try:
            con = pyodbc.connect('Driver={SQL Server};''Server=sqlerp;'
                             'Database=Bavaria;''Trusted_Conection=yes;'
                             'uid=sa;''pwd=;')
            cursor = con.cursor()
            print('Auth Ok Database')
            return cursor
        except:
            print('Ocurrio un problema en la autenticacion al servidor')
    
    
    def search_user(self,name):
        if self.cursor:
            SQL = 'SELECT * FROM USUARIO WHERE NOMBRE LIKE ?'
            Param = f'%{name}%'
            info = self.cursor.execute(SQL,Param)
            if info:
                for row in info:
                    print(row)
c = intelisis()
c.search_user('Gerson')        