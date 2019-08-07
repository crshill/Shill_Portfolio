# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 12:38:45 2019

@author: LGC0069
"""

import numpy as np
#import tkinter.ttk as ttk
#from GUI import *
#rt = ttk.Tk()
#gui = CoreGUI(rt)

import pandas as pd
import pyodbc
from datetime import datetime
import datetime as dt


def load_data(server, dat) :
        
    cnxn = pyodbc.connect('DRIVER={SQL Server};UID=LGC0069;WSID=LGC-5CG62446DY;Trusted_Connection=Yes;SERVER='+server+';DATABASE='+dat)
        
        
        
    query1 = "SELECT [Name],[UnitCode],[UnitClassification] FROM Unit"
    query2 = "SELECT [UnitCode],[AuditYear],[CreateDatetime],[IntergovernmentalSourceCode] FROM UnitDetail"


    df = pd.read_sql(query1, cnxn)
    df = df.drop_duplicates()
        
    df1 = pd.read_sql(query2, cnxn)
    df1 = df1.loc[df1['AuditYear']==2018]
    df1 = df1.drop_duplicates()

    df = pd.merge(df,df1,how = 'right', on='UnitCode')
    df = df.drop_duplicates(subset={'UnitCode','AuditYear','IntergovernmentalSourceCode'})
    df['CreateDatetime']=df['CreateDatetime'].astype('datetime64[ns]')
    df = df.loc[(df['UnitClassification'].isin(['A','B']))]
    df = df.loc[df['IntergovernmentalSourceCode'] == 'AFIR']
    df = df.sort_values('Name')
    df_out = df['Name'].str.upper()
    print('finished loading names')
        
    return df_out


def load_report() :
        
    cy = 2018
    fy = cy - 2
    years = range(fy,cy + 1)
        

        
    audit_sub_dt = np.array([])
    yrs = np.array([])
    names = np.array([])


    
        
    for y in years :
            
        aud = pd.read_excel('L:Unit Adm. Documents/'+str(y)+' Unit Audit Assignment Log.xlsx', 
                            sheet_name = 'Assignment Log', skiprows=1)
        aud = aud.loc[aud['Unit Type'].isin([50,51]),{'Unit Name', 'Date Report submitted in Portal '}]
        aud['Unit Name'] = aud['Unit Name'].str.upper()
        late = dt.date(y,12, 1)
        never = dt.date(y+1,6,30)
            
        munics = aud['Unit Name']
        for munic in munics :  
            print(munic)
            aus = aud.loc[aud['Unit Name'] == munic, 'Date Report submitted in Portal '].values
            
            if isinstance(aus[0], datetime) :
                print('dt')
                aus = aus[0].date()
            elif isinstance(aus[0], np.datetime64) :
                print('np')
                ts = (aus[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
                aus = datetime.utcfromtimestamp(ts).date()
            else :
                print(aus[0])
                aus = aus[0]
            #aus = dt.parse(str(aus[0]))
            if aus == datetime.utcfromtimestamp(0) or aus == '#N/A' or aus == '' or isinstance(aus, float) :
                audit_sub_dt = np.append(audit_sub_dt, [0])
            elif aus > late and aus < never : #submit date after 6/30/next year
                audit_sub_dt = np.append(audit_sub_dt, [0.5])   
            elif aus > never :
                audit_sub_dt = np.append(audit_sub_dt, [0])   
            else:
                audit_sub_dt = np.append(audit_sub_dt, [1])

            names = np.append(names, [munic])
            yrs = np.append(yrs, [y])
            

        print(y)
                
    subs = pd.DataFrame({'Municipality': names, 'AuditYear':yrs, 'Audit Submitted':audit_sub_dt,})
    subs = subs.pivot(index = 'Municipality', columns='AuditYear', values='Audit Submitted')
        


    return subs

#df = load_data('SQLMSCP3','SLG_Reporting')
out = load_report()
out.to_csv('~/Documents/Projects/Municipal Systems/Data/Audit_Submit_History.csv')


#ts = (aus[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')

#datetime.utcfromtimestamp(ts)