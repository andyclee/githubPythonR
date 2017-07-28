import database

import datetime

import numpy as np

from sklearn import linear_model

"""
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
"""

"""
Next section is for determining what the best gamma and C
values for the RFB are
"""

#Returns dict of numpy arrays keyed by language
def getNumpyArrays(queryName):
    result = database.getData(queryName)
    npResults = {}

    for langType in result.keys():
        npResults[langType] = np.asarray(result[langType])

    return npResults



"""
While RFB is probably better for time series prediction,
however because our data set is extremely small
and does not have any 'seasonal' fluctuations, an
RBF may not be entirely necessary and may prove to be
impractical given the simplicity of the dataset
Especially considering the dataset, RBF is extremely
prone to overfitting

Instead, a simple linear model will be used in order
to avoid overfitting
"""

def getLinRegPred(array, predYears):
    splitArr = np.hsplit(array, 2)
    x = splitArr[0]
    y = splitArr[1]
    y = y.ravel()
    linModel = linear_model.LinearRegression()

    linModel.fit(x, y)

    curYear = datetime.datetime.now().year
    lastPredYear = curYear + predYears

    years = np.arange(curYear, lastPredYear)
    years = years.reshape(-1, 1)

    return linModel.predict(years)

"""
#Gets best gamma and C for a single numpy array
def getRFBParams(array):
    splitArr = np.hsplit(array, 2)
    x = splitArr[0]
    y = splitArr[1]
    
    scaler = StandardScaler()
    x = scaler.fit_transform(x)

    y = y.ravel()

    C_range = [1e-2, 1, 1e2]
    gamma_range = [1e-1, 1, 1e1]

    param_grid = {'C': C_range, 'gamma' : gamma_range}
    gridSearch = GridSearchCV(SVC(kernel='rbf'), param_grid)
    gridSearch.fit(x, y)
    print("The best parameters are %s with a score of %0.2f"
          % (gridSearch.best_params_, gridSearch.best_score_))
    curBest = 0
    bestParams = (0, 0)
    for C in C_range:
        for gamma in gamma_range:
            clf = SVC(C=C, gamma=gamma)
            clf.fit(x, y)
            clfScore = clf.score(x, y)
            if (clfScore > curBest):
                curBest = clfScore
                bestParams = (gamma, C)

    return bestParams

def createRFBModel(array, params, predYears):
    splitArr = np.hsplit(array, 2)
    x = splitArr[0]
    y = splitArr[1]
    y = y.ravel()

    scalerX = StandardScaler()
    scalerY = StandardScaler()
    xScaled = scalerX.fit_transform(x)
    yScaled = scalerY.fit_transform(y)

    print(params[1])
    clfRBF = SVC(gamma=params[0], C=params[1], kernel='rbf')

    curYear = datetime.datetime.now().year
    lastPredYear = curYear + predYears

    predYears = np.arange(curYear, curYear + 8)
    predYears = predYears.reshape(-1, 1)

    print(x)
    print(y)

    clfRBF.fit(xScaled, yScaled)
    pred = clfRBF.fit(scalerX.transform(predict))
    pred = scalerY.inverse_transform(pred)

    print(pred)

    lw = 2
    plt.scatter(x, predYears, color='darkorange', label='data')
    plt.hold('on')
    plt.plot(x, pred, color='navy', lw=lw, label='RBF model')
    plt.xlabel('years')
    plt.ylabel('number of repos')
    plt.title('Language')
    plt.legend()
    plt.show()

"""
