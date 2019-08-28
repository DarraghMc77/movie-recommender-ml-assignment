#pylint: disable=C0103, C0111
import time
from surprise import SVD
from surprise import Dataset
from surprise import dataset
from surprise import evaluate, print_perf
import numpy as np
import matplotlib.pyplot as plt

def GetStats(name, values):
    std_dev = np.std(values)
    mean = np.mean(values)
    conf_interval = 1.645*(std_dev/folds**0.5)
    print("%s\nMEAN: %f\nCONFIDENCE INTERVAL: %f\n" % (name, mean, conf_interval))

    return mean, conf_interval

def DoGraph(val1, val2, interval1, interval2):
    ind = np.arange(1)
    width = 0.35
    fig, ax = plt.subplots()

    rects1 = ax.bar(ind, val1, width, color='r', yerr=interval1)
    rects2 = ax.bar(ind+width, val2, width, color='y', yerr=interval2)

    ax.legend((rects1[0], rects2[0]), ('RMSE', 'MAE'))
    ax.set_ylabel('Error')
    ax.set_title('Error Rates of SVD')
    plt.show()
    plt.savefig("error.png")

if __name__ == "__main__":
    start_time = time.time()

    folds = 5
    reader = dataset.Reader(line_format='user item rating', sep='\t')
    data = Dataset.load_from_file('movielens100k/ml-100k/u.data', reader)
    data.split(n_folds=folds)

    # We'll use the famous SVD algorithm.
    algo = SVD()

    # Evaluate performances of our algorithm on the dataset.
    perf = evaluate(algo, data, measures=['RMSE', 'MAE'])
    print("\n\n--- Time Elapsed: %s seconds ---" % (time.time() - start_time))

    rmse = np.array(perf['rmse'])
    mae = np.array(perf['mae'])

    rmse_mean, rmse_conf_interval = GetStats("RMSE", rmse)
    mae_mean, mae_conf_interval = GetStats("MAE", mae)

    print_perf(perf)
    DoGraph(rmse_mean, mae_mean, rmse_conf_interval, mae_conf_interval)
