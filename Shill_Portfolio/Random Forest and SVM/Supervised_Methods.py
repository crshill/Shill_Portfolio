
"""
Here are a set of supervised machine learning algorithms:
    Random Forest Classifier - runs through given file
    Random forest classifier - Uses given file to train then predict another file
    Random Forest Feature Selection
    Suport Vector Machine
    
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Normalizer
from sklearn import svm
# noinspection PyDeprecation
# from sklearn.cross_validation import train_test_split


class S_Models(object) :

# This is a routine that utilizes a random forest classifier to predict the rating of all given WUSs by cycling through
# the entire set of municipalities using a given step size. Where (total # of WUSs) mod step = 0
# Put in machine learning terms, this is k-fold cross validation (where k = (# of WUSs)/step)

    def classifier_step(self, file, step) :

        data = pd.read_csv(file)
        features = list(data.columns[1:-1])
        print(features)
        this = {"Municipality" : [], "Given" : [], "Model" : []}
        out = pd.DataFrame(this)
        NN = len(data)/step

        for nn in range(NN) :

            b = step*nn
            e = b+step

            test = data.iloc[b:e]
            train = pd.merge(data.iloc[:b], data.iloc[e:], how='outer')

            y = train["Rating"]
            x = train[features]

            scaler = Normalizer().fit(x)
            normalizedx = scaler.transform(x)

            test = test.reset_index(drop = True)
            clf = RandomForestClassifier(n_estimators=3000)
            clf = clf.fit(normalizedx, y)

            for i in range(len(test["Municipality"])) :

                #print(data.iloc[i, 1:-1])
                answer = clf.predict([test.iloc[i, 1:-1]])
                if answer == 5 :
                    a = "Prosperous"
                elif answer == 4 :
                    a = "Sustaining"
                elif answer == 3 :
                    a = "Uncertain/ Nuetral"
                elif answer == 2 :
                    a = "Unsustainable"
                else :
                    a = "Failing"

                print("{0} is {1}".format(test.get_value(i, 'Municipality'), a))
                out = out.append([[test.get_value(i, "Municipality"), test.get_value(i, "Rating"), answer[0]]], ignore_index=True)

        #out.to_csv("./Sustainability_new.csv")

        return out

#file = "./Data/Final_Rating_Data_D.csv"
####################################################################
####################################################################
# df - designated file. Similar to the previous routine, this uses a random forest classifier to predict the ratings of
# a given set of WUSs. This routine, however, takes two files as input, using file1 as the data to train the model, and
# file2 as the test data whos ratings will be predicted.


    def classifier_df(self, file1, file2) :

        data = pd.read_csv(file1)
        removed = pd.read_csv(file2)
        features = list(data.columns[1:-1])
        print(features)
        this = {"Municipality" : removed["Municipality"], "Given" : np.zeros(len(removed["Municipality"])),
                    "Model" : np.zeros(len(removed["Municipality"]))}
        out = pd.DataFrame(this)

        y = data["Rating"]
        x = data[features]

        clf = RandomForestClassifier(n_estimators=5000)
        clf = clf.fit(x, y)

        for i in range(len(removed["Municipality"])) :

            #print(data.iloc[i, 1:-1])

            answer = clf.predict([removed.iloc[i, 1:-1]])
            if answer == 5 :
                a = "Prosperous"
            elif answer == 4 :
                a = "Sustaining"
            elif answer == 3 :
                a = "Uncertain/ Nuetral"
            elif answer == 2 :
                a = "Unsustainable"
            else :
                a = "Failing"

            print("{0} is {1}".format(removed.get_value(i, 'Municipality'), a))

            #out = out.append([[removed.get_value(i, "Municipality"), removed.get_value(i, "Rating"), answer[0]]])
            #out = out.set_value(i,"Municipality",removed.get_value(i, "Municipality"))

            out = out.set_value(i, "Given", removed.get_value(i, "Rating"))
            out = out.set_value(i, "Model", answer[0])

        out.to_csv("./Sustainability_Of_Note.csv")


########################################################################
########################################################################
# Feature Selection routine that will return an normalized, ordered list of the fields that correlate most with
    # the independent variable. For instance, population has the largest correlation with WUS rating with a coefficient
    # of approx. ~0.35. Adding all coefficients will return 1 (normalized).


    def feature_select(self, file1) :


        #normed = pd.read_csv(file2)
        data = pd.read_csv(file1)

        #data = pd.merge(normed, reg, how='outer', on='Municipality')
        #print(data.head())

        features = list(data.columns[1:-1])
        print(features)

        x = data[features]
        y = data["Rating"]

        rf = RandomForestRegressor(n_estimators=5000)
        rf.fit(x, y)
        print("Features sorted by their score:")
        print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), features), reverse=True))


########################################################################
########################################################################
    # SVM - Support Vector Machine. This routine attempts to classify each municipality relative to the rating system,
    # by grouping municipalities based on their position in phase space according to the data.
    # Types of svm: RBF, linear, poly (polynomial)

    def svm_class(self, file) :

        data = pd.read_csv(file)
        outy = {"Munic": [], 'Rating': []}
        out = pd.DataFrame(outy)

        features = list(data.columns[1:-1])
        print(features)

        X = data[features]
        Y = data["Rating"]

        C = 1.0
        svc = svm.SVC(kernel='rbf', C=C).fit(X, Y)

        for m in data['Municipality'] :
            munic_data = data.loc[data['Municipality'] == m][features]
            r = svc.predict(munic_data)
            print(m, ", ", r)
            aa = {'Munic': [m], 'Rating': [r]}
            add = pd.DataFrame(aa)

            out = pd.concat([out, add])

        data.rename(columns = {'Rating':'Given'})
        #ut = pd.concat([out, data['Given']], axis = 1)

        out.to_csv('./Model/SVM_Rating.csv')



