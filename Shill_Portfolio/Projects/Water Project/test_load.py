# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:26:15 2019

@author: LGC0069
"""

import pandas as pd

mnc = pd.read_excel('~/Documents/Projects/Municipal Systems/Data/Munics_and_Counties.xlsx')
mnc = mnc.loc[:, {'Municipality', 'County', 'UnitClassification'}]
aud = pd.read_csv('~/Documents/Projects/Municipal Systems/Data/Audit_Submit_History.csv')

aud = pd.merge(aud, mnc, how = 'left', on = 'Municipality')

aud.to_excel('~/Documents/Projects/Municipal Systems/Data/Audit_Submit_History_wCounties.xlsx')

"""
This is for making a file of all municipalities with their corresponding counties.
"""

#import pyodbc
#
#server = 'SQLMSCP3'
#dat = 'SLG_Reporting'
#
#cnxn = pyodbc.connect('DRIVER={SQL Server};UID=LGC0069;WSID=LGC-5CG62446DY;Trusted_Connection=Yes;SERVER='+server+';DATABASE='+dat)
#        
#        
#query1 = "SELECT [Name],[UnitCode],[UnitClassification] FROM Unit"
#query2 = "SELECT [UnitCode],[DominantCounty] FROM UnitDominantCounty"
#
#munics = pd.read_sql(query1, cnxn)
#munics = munics.loc[munics['UnitClassification'].isin(['A','B'])]
#munics= munics.drop_duplicates()
#
#        
#df1 = pd.read_sql(query2, cnxn)
#df1 = df1.drop_duplicates()
#
#
#munics = pd.merge(munics, df1, how = 'left', on = 'UnitCode')
#counties = munics.loc[munics['UnitClassification'] == 'B', {'UnitCode', 'Name'}]
#
##munics = munics.dropna()
#
#counties = counties.rename(index=str, columns={'Name':'County', 'UnitCode':'DominantCounty'})
#counties.to_excel('~/Documents/Projects/Municipal Systems/Data/Counties.xlsx')
#munics = pd.merge(munics, counties, how ='left', on = 'DominantCounty')
#munics = munics.drop_duplicates()
#
#munics.to_excel('~/Documents/Projects/Municipal Systems/Data/Munics_and_Counties.xlsx')
