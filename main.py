# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:10:41 2021

@author: Rogelio
"""

import argparse
from model import auth,update_nomina

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
    uid = conexion.authentic()
    if uid:
        while True:
            print('Welcome to Odoo Tool')
            print('Select to option')
            print('1 -  Payroll Update')
            print('2 -  Reset all attendences')
            print('0 -  Exit')
            op = input('>  ')
            if op == '0':
                print('Ok! Bye')
                break
            elif op == '4':
                odoo_op = update_nomina.odoo(uid=uid,clave=arguments.password,db=arguments.db,host=arguments.host)
                odoo_op.users()
            elif op == '2':
                odoo_op = update_nomina.odoo(uid=uid,clave=arguments.password,db=arguments.db,host=arguments.host)
                odoo_op.reset_attendence()
            elif op == '1':
                odoo_op = update_nomina.odoo(uid=uid,clave=arguments.password,db=arguments.db,host=arguments.host)
                odoo_op.update_journal()
                odoo_op.update_structure()
                odoo_op.update_all_rules()
            else:
                print('Opcion no valida!')
                break

if __name__ == '__main__':
    arguments = parser()
    main(arguments)
