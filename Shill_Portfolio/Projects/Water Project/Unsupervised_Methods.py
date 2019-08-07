# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:44:31 2019

Here are a set of unsupervised machine learning algorithms.
Namely:
    k-means clustering

@author: Chris Shill

"""

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
#from numpy import random, float


class US_Models(object) :

    """
    This is a k-means clusterig model that takes a numerical file and lumps
    each data point into one of k clusters.
    """
    def kmeans(self, file, k) :
        data = pd.read_csv(file, index_col='MunicYear')
        #names = data["Municipality"].values
        features = data.columns.values
        nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
                'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
                'fifteen', 'sixteen', 'seventeen', 'eighteen', 'ninteen',
                'twenty', 'twentyone']
        
        #nums = ['one', 'two', 'three', 'four', 'five']
        print(features)
        #X = data[features]
        #X = X.replace(0,np.NaN)
        data = data.replace(0,np.NaN)
        
        out = pd.DataFrame({'MunicsYear':data.index.values})
        
        model = KMeans(n_clusters=k, n_init = 50)
        
        #for f in range(len(features)):
            
            #feats = features[:f+1]
        x = data[features]
        x.dropna(inplace=True)
        print(x.head())
            
        names = x.index.values
        # Note I'm scaling the data to normalize it! Important for good results.
        model = model.fit(scale(x))
            
        en = pd.DataFrame({'MunicsYear':names, 'Rating': model.labels_})
            

        # We can look at the clusters each data point was assigned to
        #print(model.labels_)
        
        out = pd.merge(out, en, how = 'left', on = 'MunicsYear')
        out.to_csv('./Model/Kmeans_ratings_byYear(3).csv')

