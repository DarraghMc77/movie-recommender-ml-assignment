#pylint: disable=C0103, C0111
import time
from surprise import SVD
from surprise import Dataset
from surprise import dataset
from surprise import evaluate, print_perf, accuracy, Reader, Prediction
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
import sys
import pandas as pd

def GetStats(name, values):
    std_dev = np.std(values)
    mean = np.mean(values)
    conf_interval = 1.645*(std_dev/folds**0.5)
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
    ax.set_title('Error Rates of SVD')
    plt.savefig("svd.png")

    plt.show()

if __name__ == "__main__":
    start_time = time.time()

    # Normailise dataset
    header = ['user', 'item', 'rating', 'timestamp']
    ratings_data = pd.read_csv('movielens100k/ml-100k/u.data', sep='\t', names=header)
    ratings_data.rating = (ratings_data.rating / 5.0)
    ratings_data.to_csv("./normalised_movielens.data", sep='\t', index=False, header=False)

    folds = 5
    reader = dataset.Reader(line_format='user item rating', sep='\t', rating_scale=(0,1))
    data = Dataset.load_from_file('./normalised_movielens.data', reader)
    data.split(n_folds=folds)

    # We'll use the famous SVD algorithm.
    algo = SVD()

    rsquared_folds = np.zeros(folds)
    rmse_folds = np.zeros(folds)
    mse_folds = np.zeros(folds)
    fold = 0
    for trainset, testset in data.folds():
        start_time2 = time.time()

        # train and test algorithm.
        algo.train(trainset)
        predictions = algo.test(testset)

        print("\n\n--- Time Elapsed: %s seconds ---" % (time.time() - start_time2))

        preds = []
        truths = []
        for pred in predictions:
            preds.append(pred.est)
            truths.append(pred.r_ui)

        # Compute and print R-Squared
        rsquared = metrics.r2_score(truths, preds)
        norm_rsquared = rsquared
        print("R-Squared: %f" % norm_rsquared)
        rsquared_folds[fold] = norm_rsquared

        # Compute and print Root Mean Squared Error
        rmse = accuracy.rmse(predictions, verbose=True)
        norm_rmse = rmse
        print("RMSE: %f" % norm_rmse)
        rmse_folds[fold] = norm_rmse

        # Compute and print MAE
        # mae = accuracy.mae(predictions, verbose=True)
        mse = metrics.mean_squared_error(truths, preds)
        norm_mse = mse
        print("MSE: %f" % norm_mse)
        mse_folds[fold] = norm_mse

        fold += 1


    # Evaluate performances of our algorithm on the dataset.
    print("\n\n--- Overall Time Elapsed: %s seconds ---" % (time.time() - start_time))

    rmse_mean, rmse_conf_interval = GetStats("RMSE", rmse_folds)
    mse_mean, mse_conf_interval = GetStats("MAE", mse_folds)
    r2_mean, r2_conf_interval = GetStats("R-Squared", rsquared_folds)

    DoGraph(rmse_mean, mse_mean, r2_mean, rmse_conf_interval, mse_conf_interval, r2_conf_interval)
