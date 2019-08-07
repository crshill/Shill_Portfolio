# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:49:04 2019

@author: Chris Shill
"""

import os
import io
import numpy
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


"""
Given a file path, this function will parse all files in that path 
and seperate the text in the file.

InBody allows for using the body of say an email that contains an
unecesary header in the first line. 
"""
def readFiles(path):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root, filename)

#            inBody = False
            lines = []
            f = io.open(path, 'r', encoding='latin1')
            for line in f:
                lines.append(line)


#                if inBody:
#                    lines.append(line)
#                elif line == '\n':
#                    inBody = True
            
            
            f.close()
            message = '\n'.join(lines)
            yield path, message

"""
We are setting up a naive bayes classifier, so this uses the first algorithm
to compile the messages with a corresponding class, and uses the filename as 
the index.

"""
def dataFrameFromDirectory(path, classification):
    rows = []
    index = []
    for filename, message in readFiles(path):
        rows.append({'message': message, 'class': classification})
        index.append(filename)

    return DataFrame(rows, index=index)


"""
Takes a path to a folder containing various folders of different 
classes, a list of which are also given as an input, to build a model
to predict the class of a message relative to the messages in the path.
"""

def naive_bayes(paths,classes) :

    data = DataFrame({'message': [], 'class': []})

    for cl in classes :
        for path in paths :
            p = path + cl
            data = data.append(dataFrameFromDirectory(p, cl))


    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(data['message'].values)

    classifier = MultinomialNB()
    targets = data['class'].values
    classifier.fit(counts, targets)
    
    hope = input("Please supply to path to the messages you wish to classify: ")
    hope_counts = vectorizer.transform(hope)
    classify = classifier.predict(hope_counts)
    
    print(classify)
    return classify


