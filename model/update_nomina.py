# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 00:52:32 2021

@author: usuario
"""

from xmlrpc import client
from . import excel
from os.path import dirname, abspath
import numpy as np

class odoo:

    def __init__(self,uid,clave,db,host):
        self.uid = uid
        self.clave = clave
        self.db = db
        self.host = host
        self.default_method = '/xmlrpc/2/object'
        self.server = client.ServerProxy(self.host+self.default_method,verbose=False)

    def custom(self,**kwargs):
        self.server.execute_kw(
            self.db
            ,self.uid
            ,self.clave
            ,kwargs['model']
            ,kwargs['method']
            ,kwargs['domain'])

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

    def unlink(self,**kwargs):
        self.server.execute_kw(
            self.db
            ,self.uid
            ,self.clave
            ,kwargs['model']
            ,kwargs['method']
            ,kwargs['domain'])


    def write(self,**kwargs):
        self.server.execute_kw(
            self.db
            ,self.uid
            ,self.clave
            ,kwargs['model']
            ,kwargs['method']
            ,kwargs['domain'])

    def users(self,**kwargs):
        users1 = self.read(model='crm.team',method='search_read'
                         ,domain=[[]]
                         ,fields={'fields':['name','company_id']})
        for user in users1:
            print(user)

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


    def reset_attendence(self):
        """
        **********************************************************************
        DELETE ALL HR ENTRY WORK FOR ALL EMPLOYEES
        **********************************************************************
        """
        hr_work_entry = self.read(model='hr.work.entry',method='search_read',
                                  domain=[[]],fields={'fields':['name']})
        print('Inicio a elimiar')
        if hr_work_entry:
            for hwe  in hr_work_entry:
                self.unlink(model='hr.work.entry',method='unlink',domain=[[hwe['id']]])

        company_ids = self.read(model='res.company',method='search_read',
                                  domain=[[]],fields={'fields':['name']})
        print('Termino a elimiar')
        calendars={}
        for company_id in company_ids:
            res = self.read(model='resource.calendar',method='search_read',
                                  domain=[[['company_id','=',company_id['id']],
                                ['name', 'like','Estandar 44 horas/semana ']]]
                                ,fields={'fields':['name','company_id']})
            if res:
                calendars[res[0]['company_id'][0]] = res[0]['id']


        contracts = self.read(model='hr.contract',method='search_read',
                              domain=[[]],fields={'fields':['name','company_id','employee_id']})

        for contract in contracts:
            print(contract)
            if contract['company_id'][0] in calendars:
                self.write(model='hr.contract',method='write',domain=[[contract['id']],
                {'date_generated_from':'2021-04-21','date_generated_to':'2021-04-21'
                 ,'resource_calendar_id':calendars[contract['company_id'][0]]}])
                if contract['employee_id']:
                    self.write(model='hr.employee',method='write',domain=[[contract['employee_id'][0]],
                    {'resource_calendar_id':calendars[contract['company_id'][0]]}])

        """
        ***********************************************************************
        GENERATE ATTENDANCE
        **********************************************************************
        """
        #employees = self.read(model='hr.employee',method='search_read',
        #                      domain=[[]],fields={'fields':['name']})
        #print(employees)
        #for employee in employees:
        #    self.custom(model='hr.employee',method="generate_work_entries",
        #                domain=[employee['id'],'2021-04-21','2021-04-21'])

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

    def update_all_rules(self):
        files = []
        files.append({'path':'/data/anticipo.xlsx','tipo':'anticipo'})
        files.append({'path':'/data/mensual.xlsx','tipo':'mensual'})
        for file in files:
            self.update_rule(filename=file['path'],tipo_estructura=file['tipo'])

    def update_rule(self,filename,tipo_estructura):
        structure = self.read(model='hr.payroll.structure',method='search_read'
                             ,domain=[[['name','ilike',tipo_estructura]]]
                             ,fields={'fields':['name','company_id']})
        root = dirname(dirname(abspath(__file__)))
        my_file = excel.Excel()
        result = my_file.read_file(file=root+filename)
        for struct in structure:
            for r in result:
                rule = self.read(model='hr.salary.rule',method='search_read',
                        domain=[[['struct_id','=',struct['id']],['code','=',r[0]]]]
                        ,fields={'fields':['name','struct_id','code']})
                if rule:
                    keys = {1:'account_debit',2:'account_credit',3:'amount_python_compute'}
                    insert_dict = {}
                    for c in r:
                        if r.index(c) > 0:
                            if str(type(c)) == "<class 'str'>":
                                if r.index(c) in [1,2]:
                                    account = self.read(model='account.account'
                                    ,method='search_read'
                                    ,domain=[[['code','=',c]
                                    ,['company_id','=',struct['company_id'][0]]]]
                                    ,fields={'fields':['name','company_id']},limit=1)
                                    insert_dict[keys[r.index(c)]]=account[0]['id']
                                else:
                                    insert_dict[keys[r.index(c)]]=c
                    print(insert_dict)
                    if insert_dict:
                        print('final_update')
                        self.write(model='hr.salary.rule',method='write'
                            ,domain=[[rule[0]['id']],insert_dict])
