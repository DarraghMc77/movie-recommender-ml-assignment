import math
import pandas
import numpy as np
import inspect
import sys
import time
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn import datasets, linear_model
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from contentbased_linear import init

start_time = 0

def GetStats(name, values):
    std_dev = np.std(values)
    mean = np.mean(values)
    conf_interval = 1.645*(std_dev/5**0.5)
    print("%s\nMEAN: %f\nCONFIDENCE INTERVAL: %f\n" % (name, mean, conf_interval))

    return mean, conf_interval

def DoGraph(val1, val2, val3, interval1, interval2, interval3):
    ind = np.arange(1)
    width = 0.35
    fig, ax = plt.subplots()

    rects1 = ax.bar(ind, val1, width, color='r', yerr=interval1)
    rects2 = ax.bar(ind+width, val2, width, color='y', yerr=interval2)
    rects3 = ax.bar(ind + width + width, val3, width, color='b', yerr=interval3)

    plt.ylim(ymin=0)
    plt.ylim(ymax=0.5)

    ax.axes.get_xaxis().set_visible(False)

    ax.legend((rects1[0], rects2[0], rects3[0]), ('RMSE', 'MSE', 'R-Squared'))
    ax.set_title('Error Rates of Linear Regression')
    plt.savefig("linreg.png")

    plt.show()

# Returns the test and training input and output rows based on indexes from KFolds
# fileDetails is passed through from __main__ and contains the Dicts in 'inputFiles'
# so parameters such as the column number of 'Target' can be passed via this Dict
# The Target Column number can be passed explicitly as the same file can have different
# targets columns for different algorithms
def getRowsandColumns(dataFrame, train_index, test_index, fileDetails, target):
    excludeCols = fileDetails["excludeColumns"]

    # get a list described y the range given in 'fileDetails["featureColumns"]' with
    # elements of fileDetails["excludedCols"] list excluded
    featureCols = [x for x in range(fileDetails["featureColumns"][0], fileDetails["featureColumns"][1])]

    Xtrain = dataFrame.iloc[train_index,featureCols]
    Xtest = dataFrame.iloc[test_index,featureCols]

    ytrain = dataFrame.iloc[train_index,target]
    ytest = dataFrame.iloc[test_index,target]
    return (Xtrain,ytrain, Xtest,ytest)

# returns the name of the calling function; used for inspecting which algo is being called to print
# the name into the CSV
def thisFunc():
    return inspect.stack()[1][3] 

def linearRegression(dataFrame, train_index, test_index, fileDetails):
    (Xtrain,ytrain,Xtest,ytest) = getRowsandColumns(dataFrame, train_index, test_index, fileDetails, fileDetails["targetColumn"])
    lr = linear_model.LinearRegression(normalize=True)
    lr.fit(Xtrain,ytrain)

    our_metrics = {}
    predictions = lr.predict(Xtest)
    print("Average rating: " + str(float(sum(predictions))/len(predictions)))

    mse = mean_squared_error(ytest,[x for x in predictions])
    r2 = lr.score(Xtest,ytest)
    rmse = math.sqrt(mse)

    our_metrics['RMSE'] = rmse
    our_metrics['MSE'] = mse
    our_metrics['R2'] = r2

    print(lr.get_params())
    return our_metrics

# for each function in the 'algorithms' list, run the function on each dataset listed in the inputFiles list.
# Each dataset was split into the correct number of sub-sets by parseCSV()
# Each function in 'algorithms' should return a dict with a Key describing the metric name, and a Value
# which is the result of metric
# e.g. {RMSE:"123", "MAE":300}
#
# metricAverages{} will then contain a key of tuple (algorithm,metric), and a value which is
# a list of metrics for each dataFrame size.
# e.g. metricAverages = { (linearRegression, RMSE): [23,34,67,99], (linearRegression,MAE):[12,3,5] }
# This is used to create the output CSV file
#algorithms = [linearRegression, logisticRegression, huberRegression]
def splitAndTrain(dataFrame_list, datasetName, fileDetails):
    metricAverages = {}

    kf = KFold(n_splits=5)
    for dataFrame in dataFrame_list:
        print("Processing dataframe of size %d" % len(dataFrame))
        i=0
        algorithm = linearRegression
        metricsPerAlgorithm = {}
        for train_index, test_index in kf.split(dataFrame):
            print("\n-------\nFold" + str(i))
            metricsDict = algorithm(dataFrame, train_index, test_index, fileDetails)
            for metric, value in metricsDict.items():
                try:
                    metricsPerAlgorithm[metric].append(value)	
                except KeyError:
                    metricsPerAlgorithm[metric] = [value]
                print(str(metric) + ":  " + str(value))
            i+=1
        print("\n\n--- Time Elapsed: %s seconds ---" % (time.time() - start_time))

        print(metricsPerAlgorithm)
        rmse_mean, rmse_conf_interval = GetStats("RMSE", metricsPerAlgorithm["RMSE"])
        mse_mean, mse_conf_interval = GetStats("MSE", metricsPerAlgorithm["MSE"])
        r2_mean, r2_conf_interval = GetStats("R-Squared", metricsPerAlgorithm["R2"])

        DoGraph(rmse_mean, mse_mean, r2_mean, rmse_conf_interval, mse_conf_interval, r2_conf_interval)

        for metric, valueList in metricsPerAlgorithm.items():
            try:
                metricAverages[(algorithm.__name__, metric)].append( sum(valueList)/float(len(valueList)))
            except KeyError:
                metricAverages[(algorithm.__name__, metric)] = [sum(valueList)/float(len(valueList))]
        i=0
    for (algorithm, metric), metricValues in metricAverages.items():
        print([algorithm + " -- " + datasetName + " -- " + metric + "," + ",".join(map(str,metricValues))])

if __name__ == "__main__":
    debugMode = False
    if debugMode:
        print("Debug mode on, printing extra information.\nThis can be turned off in Config.py\n")
    start_time = time.time()

    dataFrame = init()
    dataFrame = dataFrame.fillna(method='ffill')

    print("data parsed")

    splitAndTrain([dataFrame],"movieLens",dict({"filePath":"","columnNameRow":0,"targetColumn":56,"featureColumns":(0,56),"excludeColumns":[],"skipFirst":True}))
