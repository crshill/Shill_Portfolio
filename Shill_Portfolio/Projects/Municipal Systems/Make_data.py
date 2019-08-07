# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:55:50 2019

@author: LGC0069
"""

import pandas as pd
import os
import numpy as np
from math import floor

def count_schools_over() :

    out = pd.DataFrame({'School District' : [], 'Number of Schools' : [], 'Number of Schools with [2] > $200k' : [],
                    'Number of Schools with [2] > $250k' : [], 'Number of Schools with [3]+[4] > $200k' : [],
                    'Number of Schools with [3]+[4] > $250k' : [], 'Number of Schools with [7] > $250k': []})
    sheets = ['2','3','4','5','6','7','8','9','10']

    path = 'G:/Debbie Tomasko/School reports/'
    
    for f in os.listdir(path) :
    
        if f.startswith('C-') :

            dat = pd.read_excel(path+f, 
                    sheetname='LGC203 - PG 1', skiprows = 7)

            sd =dat.iloc[2,6:7].values[0]
            count2_200 = 0
            count2_250 = 0
            count34_200 = 0
            count34_250 = 0
            count7_250 = 0
            schools = 0
        
            print(f)

            for s in sheets :
            
                dat = pd.read_excel(path+f, 
                    sheetname='LGC203-S PG '+s, skiprows = 2)
                dat = dat.iloc[1:93].replace(np.nan, 0)
                dat = dat.drop(['[1]','[5]'], axis=1)
                if f == 'C-HENDERSON COUNTY SCHOOLS-C813-December,2018.xlsx' :
                    dat = dat.drop([4,5])

                dat.loc[:,{'[2]','[3]','[4]','[6]','[7]'}] = dat.loc[:,{'[2]','[3]','[4]','[6]','[7]'}].astype(float)
                dat['34'] = dat['[3]'] + dat['[4]']
            
                schools += len(dat.loc[dat['[6]']>0.0])
                count2_200 += len(dat.loc[dat['[2]']>=200000.0])
                count2_250 += len(dat.loc[dat['[2]']>=250000.0])
                count34_200 += len(dat.loc[dat['34']>=200000.0])
                count34_250 += len(dat.loc[dat['34']>=250000.0])
                count7_250 += len(dat.loc[dat['[7]']>=250000.0])
            
            out = out.append(pd.DataFrame({'School District' : [sd], 'Number of Schools' : [schools], 'Number of Schools with [2] > $200k' : [count2_200],
                    'Number of Schools with [2] > $250k' : [count2_250], 'Number of Schools with [3]+[4] > $200k' : [count34_200],
                    'Number of Schools with [3]+[4] > $250k' : [count34_250], 'Number of Schools with [7] > $250k': [count7_250]}))
    
        out.to_excel('./Data/SchoolDistrict_Report_Analysis_V2.xlsx') 
        
        
def schools_banks() :
    
    out = pd.DataFrame({'School District' : [], 'Name of School' : [], 'Listed Bank' : []})
    sheets = ['2','3','4','5','6','7','8','9','10']

    path = 'G:/Debbie Tomasko/School reports/'
    
    for f in os.listdir(path) :
    
        if f.startswith('C-') :

            dat = pd.read_excel(path+f, 
                    sheetname='LGC203 - PG 1', skiprows = 7)

            sd =dat.iloc[2,6:7].values[0]
            print(f)
            
            for s in sheets :
            
                dat = pd.read_excel(path+f, 
                    sheetname='LGC203-S PG '+s, skiprows = 3)
                dat = dat.iloc[3:92]
                nums = range(60)
                
                ind = [x + floor(x/2.0) for x in nums]

                dat = dat.iloc[ind]

                dat = dat.loc[:, {'Please List both', 'Total'}]

                dat['Total'] = dat['Total'].fillna(-1)
                r = (dat['Total']>0)
                #print(r)
                #print(np.roll(r,1))
                schools = dat.loc[r,'Please List both'].values

                banks = dat.loc[np.roll(r,1), 'Please List both']
                #print(banks)
                banks = banks.iloc[range(len(schools))]
                #print(banks)
                
                #print(banks)
                #names.dropna(inplace = True)

#                if s == '2' and sd == 'Alamance Burlington School System' or sd == 'Camden County Schools':
#                    banks = banks.iloc[1:]
#                elif s == '2' and sd == 'Cleveland County Schools':
#                    banks = banks.loc[banks != 'East ']
#                    banks = banks.loc[banks != 'Alliance b']

                if not len(schools)==len(banks):
                    print(s, len(banks) - len(schools))
                
                sds = [sd for n in schools]
                #print(schools)
                add = pd.DataFrame({'School District' : sds, 'Name of School' : schools, 'Listed Bank' : banks})
                #print(add)
                out = out.append(add)
            
    out.to_excel('./Data/Schools_Banks.xlsx')
        
schools_banks()

#dat = pd.read_excel('G:/Debbie Tomasko/School reports/C-NORTHAMPTON COUNTY SCHOOLS-C838-December 31,2017.xlsx', 
#                    sheetname='LGC203-S PG 2', skiprows = 2)
#dat = dat.iloc[1:93]
#for col in ['[1]','[2]','[3]','[4]','[5]','[6]','[7]'] :
#    try :
#        dat.loc[:,col] = dat.loc[:,col].astype(float)
#        print(col+': IT WORKED')
#    except ValueError :
#        print(col+': OOPS')
     
