import database

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV

"""
Next section is for determining what the best gamma and C
values for the RFB are
"""

def getNumpyArrays(queryName, languages):
    database.loadFreshData(queryName, languages)
    result = database.getData(queryName)
    npResults = {}

    for langType in result.keys():
        npResults[langType] = np.asarray(result[langType])

    return npResults

#Gets best gamma and C for a single numpy array
def getRFBParams(array):
    splitArr = np.hsplit(array, 2)
    x = splitArr[0]
    y = splitArr[1]
    
    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    C_range = [1e-2, 1, 1e2]
    gamma_range = [1e-1, 1, 1e1]
    classifiers = []
    for C in C_range:
        for gamma in gamma_range:
            clf = SVC(C=C, gamma=gamma)
            clf.fit(x, y)
            classifiers.append((C, gamma, clf))
            print(clf.best_params_)
