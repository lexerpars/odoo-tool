# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:27:42 2021

@author: Rogelio
"""

from xmlrpc import client

class Conexion:
    
    def __init__(self,usuario,clave,db,host):
        self.usuario = usuario
        self.clave = clave
        self.db = db
        self.host = '{}/xmlrpc/2/common'.format(host)
    
    def authentic(self):
        login = client.ServerProxy(self.host)
        uid = login.authenticate(self.db,self.usuario,self.clave,())
        if uid:
            print('Autenticacion exitosa ',self.usuario)
            return uid
        else:
            print('No se ha logrado autenticar al sistema')
            return False
        