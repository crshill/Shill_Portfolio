# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:18:23 2019

@author: LGC0069
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:19:08 2019

@author: LGC0069
"""

from tkinter import *
import tkinter as tk
from tkinter import messagebox
#import tkinter.ttk as ttk
#from GUI import *
#rt = ttk.Tk()
#gui = CoreGUI(rt)

import pandas as pd
import pyodbc


class reporting(object) :

    def drop_down(self, root, munics, data) :


        
        

    # Create a Tkinter variable
        tkvar = tk.StringVar(root)

    # Dictionary with options
        
        tkvar.set(munics[0]) # set the default option

        popupMenu = tk.OptionMenu(mainframe, tkvar, *choices)
        tk.Label(mainframe, text="Select the desired Municipality").grid(row = 1, column = 1)
        popupMenu.grid(row = 2, column =1)
        
        


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
        df = df.sort_values('Name')
        
        return df


    def load_report(self, df, munic) :
        
        df = df.loc[df['Name']==munic].pivot(index='AuditYear', columns='IntergovernmentalSourceCode', values='CreateDatetime')
        df = df.fillna(value='Not Submitted')
        return df
    
    
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

        
        


