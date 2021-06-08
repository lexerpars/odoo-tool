# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:10:41 2021

@author: Rogelio
"""

import argparse
from model import auth

def parser():
    pars = argparse.ArgumentParser(description='Script Odoo codigo automatiza tareas')
    pars.add_argument('login',help='Usuario de conexion a Odoo')
    pars.add_argument('password',help='Clave de autenticacion Odoo')
    pars.add_argument('db',help='Especifique la base de datos')
    pars.add_argument('host',help='Indique el host donde se aloja odoo')
    arguments = pars.parse_args()
    return arguments

def main(arguments):
    print(arguments)
    conexion = auth.Conexion(usuario=arguments.login,clave=arguments.password,db=arguments.db,host=arguments.host)
    conexion.authentic()
    
if __name__ == '__main__':
    arguments = parser()
    main(arguments)