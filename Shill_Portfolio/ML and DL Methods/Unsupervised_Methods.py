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
#import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
#from numpy import random, float


class US_Models(object) :

    """
    This is a k-means clusterig model that takes a numerical file and lumps
    each data point into one of k clusters.
    """
    def kmeans(file, k) :
        data = pd.read_csv(file)

        model = KMeans(n_clusters=k)

        # Note I'm scaling the data to normalize it! Important for good results.
        model = model.fit(scale(data))

        # We can look at the clusters each data point was assigned to
        print(model.labels_)

