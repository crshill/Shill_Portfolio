# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:59:41 2019

@author: LGC0069
"""

from Supervised_Methods import S_Models
import pandas as pd

mods = S_Models()

def main() :

    data = pd.read_exel('./Data/UAL_2015_to_2018.V2.xlsx')
    test = data.loc[data['Audit Year'] == 2018]
    test = test.drop(['Audit Year'], axis = 1)
    
    train 
    


if __name__ == '__main__' :

    main()