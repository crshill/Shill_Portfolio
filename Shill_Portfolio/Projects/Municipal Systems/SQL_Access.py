# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:27:42 2019

@author: LGC0069

Below is a script for loading in Data from a SQL server.
"""

#from sqlalchemy import create_engine
import pandas as pd
import pyodbc

class load_sql(object) :
    
    def load_data(self, server, dat, tables) :
        
        cnxn = pyodbc.connect('DRIVER={SQL Server};UID=LGC0069;WSID=LGC-5CG62446DY;Trusted_Connection=Yes;SERVER='+server+';DATABASE='+dat)

        #cursor = cnxn.cursor()
        
        #cursor.execute("SELECT * FROM UnitDetail")
        
        
        query1 = "SELECT [UnitCode],[AuditYear],[IntergovernmentalDataCode],[IntergovernmentalSourceCode],[IntergovernmentalDataValue] FROM "+tables[0]
        query2 = "SELECT [Name],[UnitCode],[UnitClassification] FROM "+tables[1]
        query3 = "SELECT [UnitCode],[UnitPopulation],[AuditYear] FROM "+tables[2]
        query4 = "SELECT [IntergovernmentalDataCode],[IntergovernmentalDataCodeDescription],[AuditYear] FROM "+tables[3]


        
        df = pd.read_sql(query1, cnxn)
        df1 = pd.read_sql(query2, cnxn)
        df2 = pd.read_sql(query3, cnxn)
        df3 = pd.read_sql(query4, cnxn)
        
        df = pd.merge(df, df1, how='left', on='UnitCode', sort = True)
        df = pd.merge(df, df2, how='left', on=['UnitCode','AuditYear'])
        df = pd.merge(df, df3, how='inner', on=['IntergovernmentalDataCode', 'AuditYear'])
        df = df.loc[(df['UnitClassification'].isin(['A','B'])) & (df['AuditYear'].isin(2016,2017,2018))]
        
        
        return df
        
        
load = load_sql()
tbls=['UnitDetail','Unit', 'UnitPopulation','IntergovernmentalData']
data = load.load_data('SQLMSCP3', 'SLG_Reporting', tbls)



print(data.columns)
print(len(data))


print(data.head(40))

#test = data.iloc[:1000]
data.to_csv('./NCSU_Data_AllMunicipalities_2016_to_2018.csv')

