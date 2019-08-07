# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:00:12 2019

@author: LGC0069
"""
import pandas as pd
import pyodbc


class UAL(object) :
    
    def query(self, srvr, db) :
        
        years = input('For which year would you like to generate a UAL?')
        
        cnxn = pyodbc.connect('DRIVER={SQL Server};UID=LGC0069;WSID=LGC-5CG62446DY;Trusted_Connection=Yes;SERVER='+srvr+';DATABASE='+db)
        
        
        query = """SELECT Name, UnitCode, UnitClassification FROM Unit"""#, UnitClassification, Population,
        #CurrentWaterSewer, CurrentElectricFund, CurrentGeneralFund FROM Unit"""
        query1 = """SELECT AuditYear, UnitCode, IntergovernmentalDataCode, IntergovernmentalDataValue,
        IntergovernmentalSourceCode FROM UnitDetail"""
        query2 = "SELECT DominantCounty, UnitCode FROM UnitDominantCounty"
        
        
        names = pd.read_sql(query, cnxn)
        names = names.drop_duplicates()
        data = pd.read_sql(query1, cnxn)
        counties = pd.read_sql(query2, cnxn)
        counties = counties.drop_duplicates()
        
        counties = pd.merge(counties, names, how = 'left', left_on = 'DominantCounty', right_on = 'UnitCode')
        counties = counties.rename(index=str, columns={'Name':'County'})
        counties = counties.drop({'UnitCode_y','UnitClassification'}, axis = 1).rename(index = int, columns = {'UnitCode_x':'UnitCode'})
        #print(counties.head())
        names = pd.merge(names, counties, how = 'left', on = 'UnitCode')
        print(names.head(20))
        
        

        
        data = data.loc[data['AuditYear']==year]
        data = data.loc[data['IntergovernmentalSourceCode']=='CCH']
        data = data.drop('IntergovernmentalSourceCode', axis = 1)
        data = data.loc[data['IntergovernmentalDataCode'].isin(['4','5','6','11','20','44','45','47',
                      '48','51','55','89','98','100','331','506','508','509','510','511','532','533',
                      '536','603','995','996'])]

        data['Unit_Year'] = data['Uni']            
        
        data = data.pivot(index = 'UnitCode', columns = 'IntergovernmentalDataCode',values='IntergovernmentalDataValue')
        data['4':'996'] = data['4':'996'].astype(float)
        df = pd.merge(names, data, how = 'left', right_index = True, left_on = 'UnitCode')
        
        df = df.loc[df['UnitClassification'].isin(['A','B'])] 
        #out.to_csv('./Data/UAL_Data.csv')
        

    
        
        df['FBA'] = df['506'] + df['536'] - df['4'] - df['5'] - df['6']
        df['FBA w/o Powell Bill'] = df['FBA'] - df['11']
        df['Total Expenditures'] = df['532'] + df['509'] + df['20'] - df['533'] - df['508']
        df['<8% FBA/Expenditures'] = df['FBA']/df['Total Expenditures']
        df['<8% FBA w/o Powell/ Expenditures'] = df['FBA w/o Powell Bill']/df['Total Expenditures']
        df['WS Quick Ratio <1'] = (df['44'] - df['510'])/df['45']
        df['WS Working Capital'] = df['44'] - df['45']
        df['Elc Quick Ratio <1'] = (df['47'] - df['511'])/df['48']
        df['Elc Working Capital'] = df['47'] - df['48']
        df['WS Cash Flow from ops less debt service'] = df['51'] - df['331'] - df['89']
        df['Elc Cash Flow from ops less debt service'] = df['55'] - df['100'] - df['98']
        #print(df.head())
        df = df.rename(index = str, columns = {'4':'GF Liabilities','5':'GF Unearned/ Defered',
                    '6':'GF Encumberances','11':'GF Powell Bill in FB','20':'GF Transfers Out','44':'WS Assets Incl. Inv. & Prepaids',
                    '45':'WS Liabilities','47':'Elc Assets Incl. Inv. & Prepaids','48':'Elc Liabilities',
                    '51':'WS Total Cash Flow from Ops','55':'Elc Cash Flow from Ops','89':'WS Interest Exp.',
                    '98':'Elc Interest Exp.','100':'Elc Pincipal Paid LTD','331':'WS Principal Paid LTD',
                    '506': 'Unrestricted C&I','508':'GF Pos. Debt Refund','509':'GF Neg Debt Refund',
                    '510':'WS Investments & Prepaids','511':'Elc Investments & Prepaids','532':'Total Expenses w/o Refund',
                    '533':'GF Proceeds LTD','536':'GF Restricted C&I','603':'Internal Control','995':'Electric Indicator','996':'WS Indicator'})
        print(df['County'].head(10))

    #print(df.columns)
        ##print(df.head())
       # writer = pd.ExcelWriter('./Data/UAL_Data_'+str(year)+'.xlsx', engine = 'xlsxwriter')
        writer = pd.ExcelWriter('./Data/UAL_Data_2015to2018.xlsx', engine = 'xlsxwriter')

        
        sheet1 = df.loc[:, {'Name','County','UnitCode','Internal Control','FBA', 'FBA w/o Powell Bill', 'Total Expenditures', '<8% FBA/Expenditures',
                            '<8% FBA w/o Powell/ Expenditures', 'WS Quick Ratio <1', 'WS Working Capital',
                            'Elc Quick Ratio <1', 'Elc Working Capital',
                            'WS Total Cash Flow from Ops',
                            'WS Principal Paid LTD', 'WS Interest Exp.', 'WS Cash Flow from ops less debt service',
                            'WS Indicator', 'Elc Cash Flow from Ops', 'Elc Pincipal Paid LTD', 'Elc Interest Exp.',
                            'Elc Cash Flow from ops less debt service', 'Electric Indicator'}]
        
        sheet2 = df.loc[:, {'Name','County','UnitCode','GF Liabilities','GF Unearned/ Defered',
                    'GF Encumberances','GF Powell Bill in FB','GF Transfers Out','WS Assets Incl. Inv. & Prepaids',
                    'WS Liabilities','Elc Assets Incl. Inv. & Prepaids','Elc Liabilities',
                    'Unrestricted C&I','GF Pos. Debt Refund','GF Neg Debt Refund',
                    'WS Investments & Prepaids','Elc Investments & Prepaids','Total Expenses w/o Refund',
                    'GF Proceeds LTD','GF Restricted C&I'}]
        
        sheet1.to_excel(writer, sheet_name='UAL Information')
        sheet2.to_excel(writer, sheet_name='All Data')
        
        writer.save()
    
ual = UAL()

ual.query('SQLMSCP3', 'SLG_Reporting')
    