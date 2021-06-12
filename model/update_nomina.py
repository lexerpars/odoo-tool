# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 00:52:32 2021

@author: usuario
"""

from xmlrpc import client
from . import excel
from os.path import dirname, abspath

class odoo:
    
    def __init__(self,uid,clave,db,host):
        self.uid = uid
        self.clave = clave
        self.db = db
        self.host = host
        self.default_method = '/xmlrpc/2/object'
        self.server = client.ServerProxy(self.host+self.default_method,verbose=False)
    
    
    def read(self,**kwargs):
        res = self.server.execute_kw(
            self.db
            ,self.uid
            ,self.clave
            ,kwargs['model']
            ,kwargs['method']
            ,kwargs['domain']
            ,kwargs['fields'])
        return res
        
        
    
    def write(self,**kwargs):
        self.server.execute_kw(
            self.db
            ,self.uid
            ,self.clave
            ,kwargs['model']
            ,kwargs['method']
            ,kwargs['domain'])
    
    def update_journal(self):
        #search default account
        account_code = '6.01.01.01.001'
        journals = self.read(model='account.journal',method='search_read'
                             ,domain=[[['name','=','Nomina']]]
                             ,fields={'fields':['name','company_id']})
        print(journals)
        for journal in journals:
            account = self.read(model='account.account',method='search_read'
                             ,domain=[[['code','=',account_code],['company_id','=',journal['company_id'][0]]]]
                             ,fields={'fields':['name','company_id']})
            print(account)
            if account:
                self.write(model='account.journal'
                                    ,method='write',domain=[[journal['id']]
                                    ,{'default_debit_account_id':account[0]['id']
                                    ,'default_credit_account_id':account[0]['id']}])
                print('update ok!')
    
    def update_structure(self):
        structure = self.read(model='hr.payroll.structure',method='search_read'
                             ,domain=[[]]
                             ,fields={'fields':['name','company_id']})
        if structure:
            for struct in structure:
                print(struct)
                journal = self.read(model='account.journal',method='search_read'
                                    ,domain=[[['name','=','Nomina']
                                    ,['company_id','=',struct['company_id'][0]]]]
                                    ,fields={'fields':['name']})
                print(journal)
                if journal:
                    self.write(model='hr.payroll.structure',method='write'
                               ,domain=[[struct['id']],{'journal_id':journal[0]['id']}])
                    print('structure update ok!')
                    
    def update_rule(self):
        structure = self.read(model='hr.payroll.structure',method='search_read'
                             ,domain=[[['name','ilike','anticipo']]]
                             ,fields={'fields':['name','company_id']})
        root = dirname(dirname(abspath(__file__)))
        my_file = excel.Excel()
        result = my_file.read_file(file=root+'/data/anticipo.xlsx')
        for r in result:
            print(r)

        
        
        
    