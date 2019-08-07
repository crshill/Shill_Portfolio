import numpy as np
import pandas as pd

def insert_a_point(file) :

    df = pd.read_csv(file)

    df1 = df.drop_duplicates('Municipality')

    for munic in df1['Municipality'] :


        df = df.append(df.loc[df['Municipality']==munic].iloc[0], ignore_index=True)
        df.loc[df['Municipality'] == munic].loc[6:6,"Path"]=7
        print(df.loc[df['Municipality'] == munic])

    df.to_csv('./Data/Data_Radial_V1.csv')


insert_a_point('./Data/Data_Radial.csv')

def change_7(file) :

    df2 = pd.read_csv(file)

    for munic in range(len(df2)) :

        if (munic+1) % 7 == 0 :
            df2 = df2.set_value(munic, 'Path', 7)


    df2.to_csv('./Data/Radar_Plot_Data_Final.csv')

#change_7('./Data/Radar_plot_data_test.csv')


