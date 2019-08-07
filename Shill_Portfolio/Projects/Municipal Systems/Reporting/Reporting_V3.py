# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:39:26 2019

@author: LGC0069
"""

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
#import tkinter.ttk as ttk
#from GUI import *
#rt = ttk.Tk()
#gui = CoreGUI(rt)

import pandas as pd
import pyodbc
import datetime as dt


class reporting(object) :

    def drop_down(self, root, munics, data) :
        
    # on change dropdown value
        def change_dropdown(*args):
            tkvar.get()

    # link function to change dropdown
        #tkvar.trace('w', change_dropdown)
        root.mainloop()
        
        return str(tkvar.get())
        
    def load_data(self, server, dat) :
        
        cnxn = pyodbc.connect('DRIVER={SQL Server};UID=LGC0069;WSID=LGC-5CG62446DY;Trusted_Connection=Yes;SERVER='+server+';DATABASE='+dat)
        
        
        
        query1 = "SELECT [Name],[UnitCode],[UnitClassification] FROM Unit"
        query2 = "SELECT [UnitCode],[AuditYear],[CreateDatetime],[IntergovernmentalSourceCode] FROM UnitDetail"


        df = pd.read_sql(query1, cnxn)
        df = df.drop_duplicates()
        
        df1 = pd.read_sql(query2, cnxn)
        df1 = df1.loc[df1['AuditYear']>=(df1['AuditYear'].max()-2)]
        df1 = df1.drop_duplicates()

        
        df = pd.merge(df,df1,how = 'right', on='UnitCode')
        df = df.drop_duplicates(subset={'UnitCode','AuditYear','IntergovernmentalSourceCode'})
        df['CreateDatetime']=df['CreateDatetime'].astype('datetime64[ns]')
        df = df.loc[(df['UnitClassification'].isin(['A','B']))]
        df = df.loc[df['IntergovernmentalSourceCode'] == 'AFIR']
        df = df.sort_values('Name')
        
        return df


    def load_report(self, df, munic) :
        
        cy = df['AuditYear'].max()
        fy = cy - 2
        years = range(fy,cy + 1)
        
        jun_sub = np.array([])
        dec_sub = np.array([])
        
        audit_sub_dt = np.array([])
        UL = np.array([])
        on_UAL = np.array([])
        
        
        for y in years :
            
            if os.path.exists('G:/SHARE/USER/LGC203/' +str(y)+ '-6-30/') :
                if os.path.exists('G:/SHARE/USER/LGC203/' +str(y)+ '-6-30/LGC 203 June 30 '+str(y)+' Database.xlsm') :
                    jun203 = pd.read_excel('G:/SHARE/USER/LGC203/' +str(y)+ '-6-30/LGC 203 June 30 '+str(y)+' Database.xlsm', sheet_name = 'Data Master')
                    jun203['UNIT_DESC'] = jun203['UNIT_DESC'].str.upper()
                    js = dt.datetime.date(jun203.loc[jun203['UNIT_DESC'] == munic, 'DATE_RECEIVED'].values[0])
                elif os.path.exists('G:/SHARE/USER/LGC203/' +str(y)+ '-6-30/LGC 203 June 30, '+str(y)+' Database.xlsm') :
                    jun203 = pd.read_excel('G:/SHARE/USER/LGC203/' +str(y)+ '-6-30/LGC 203 June 30, '+str(y)+' Database.xlsm', sheet_name = 'Data Master')
                    jun203['UNIT_DESC'] = jun203['UNIT_DESC'].str.upper()
                    js = dt.datetime.date(jun203.loc[jun203['UNIT_DESC'] == munic, 'DATE_RECEIVED'].values[0])
                else :
                    js = 0
                jun_sub = np.append(jun_sub, [js])
            else:
                jun_sub = np.append(jun_sub, [0])
            
            if os.path.exists('G:SHARE/USER/LGC203/' +str(y)+ '-12-31/') :
                
                if os.path.exists('G:/SHARE/USER/LGC203/' +str(y)+ '-12-31/LGC 203 December 31 '+str(y)+' Database.xlsm') :
                    dec203 = pd.read_excel('G:/SHARE/USER/LGC203/' +str(y)+ '-12-31/LGC 203 December 31 '+str(y)+' Database.xlsm', sheet_name = 'Data Master')
                    dec203['UNIT_DESC'] = dec203['UNIT_DESC'].str.upper()
                    ds = dt.datetime.date(dec203.loc[dec203['UNIT_DESC'] == munic, 'DATE_RECEIVED'].values[0])
                elif os.path.exists('G:/SHARE/USER/LGC203/' +str(y)+ '-12-31/LGC 203 December 31, '+str(y)+' Database.xlsm') :
                    dec203 = pd.read_excel('G:/SHARE/USER/LGC203/' +str(y)+ '-12-31/LGC 203 December 31, '+str(y)+' Database.xlsm', sheet_name = 'Data Master')
                    dec203['UNIT_DESC'] = dec203['UNIT_DESC'].str.upper()
                    ds = dt.datetime.date(dec203.loc[dec203['UNIT_DESC'] == munic, 'DATE_RECEIVED'].values[0])
                else :
                    ds = 0
                dec_sub = np.append(dec_sub, [ds])
            else :
                dec_sub = np.append(dec_sub, [0])
                
            if os.path.exists('L:Unit Adm. Documents/'+str(y)+' Unit Audit Assignment Log.xlsx') :
                
                aud = pd.read_excel('L:Unit Adm. Documents/'+str(y)+' Unit Audit Assignment Log.xlsx', sheet_name = 'Assignment Log', skiprows=1)
                aud['Unit Name'] = aud['Unit Name'].str.upper()
                
                aus = aud.loc[aud['Unit Name'] == munic, 'Date Report submitted in Portal '].values
                #aus = parse(str(aus[0]))
                aus = dt.datetime.date(pd.Timestamp(aus[0]).to_pydatetime())
                audit_sub_dt = np.append(audit_sub_dt, aus)
                letter = aud.loc[aud['Unit Name'] == munic, 'Unit Letter Issued'].values
                if y <= 2016 :
                    UAL = aud.loc[aud['Unit Name'] == munic, 'Watch Unit'].values
                else :
                    
                    UAL = aud.loc[aud['Unit Name'] == munic, 'Unit Assistance List'].values
                if UAL == 0 or UAL == '#N/A' or UAL == '' or UAL == np.NaN:
                    UAL = 'No'
                else :
                    UAL = 'Yes'
                on_UAL = np.append(on_UAL, [UAL])
                if letter == 'No' :
                    UL = np.append(UL, ['No'])
                else :
                    UL = np.append(UL, ['Yes'])
            else :
                audit_sub_dt = np.append(audit_sub_dt, [0])
                UL = np.append(UL, ['Not Available'])
                
                
        subs = pd.DataFrame({'AuditYear':years, 'June LGC-203 Submission Date':jun_sub,
                                 'Dec LGC-203 Submission Date': dec_sub, 'Audit Report Submission Date':audit_sub_dt,
                                 'Unit Letter Submitted': UL, 'Unit Assistance List': on_UAL})
            
                    
            
            
        
        df1 = df.loc[df['Name']==munic].pivot(index='AuditYear', columns='IntergovernmentalSourceCode', values='CreateDatetime')
        df1 = pd.merge(df1, subs, how = 'outer', on = 'AuditYear')
        df1 = df1.fillna(value='Not Submitted')
        df1 = df1.replace(to_replace = 0, value = 'Not Submitted')
        df1 = df1.set_index('AuditYear')

        return df1
    
    
    def ExitApplication(self, munic, munics, data):
        table = self.load_report(data, munic)
        table.to_excel('~/Downloads/'+munic+'_Report.xlsx')

        MsgBox = messagebox.askquestion ('Generate Another Report?','The report for '+munic+' has been saved to Downloads. Would you like to generate another report?')
        if MsgBox == 'yes':
            return 1    
            
            
        else:
            return 0
            messagebox.showinfo('Exit','The report for '+munic+' has been saved to Downloads. Exiting Application.')
            

report = reporting()
data = report.load_data('SQLMSCP3','SLG_Reporting')

munics = data['Name'].drop_duplicates()
root = tk.Tk()

root.title("Reporting - Select Municipality")

    # Add a grid
mainframe = tk.Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

choices = munics
tk.Button(root, text='Select', command=root.quit).pack()

# Create a Tkinter variable
tkvar = tk.StringVar(root)

    # Dictionary with options
        
tkvar.set(munics[0]) # set the default option

popupMenu = tk.OptionMenu(mainframe, tkvar, *choices)
tk.Label(mainframe, text="Select the desired Municipality").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)

munic = report.drop_down(root, munics, data)

cont = 1

while cont ==1 :
    cont = report.ExitApplication(munic, munics, data)
    if cont == 1 :
        munic = report.drop_down(root, munics, data)
    else: 
        root.destroy()
#print('You have selected: '+munic)



#save = rt.mainloop()

#if save :