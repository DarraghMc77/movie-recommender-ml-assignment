# pylint: disable=C0103, C0111
from math import sqrt
import numpy as np
import pandas as pd
from sklearn import cross_validation as cv
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds

header = ['user_id', 'item_id', 'rating', 'timestamp']
ratings_data = pd.read_csv('movielens100k/ml-100k/u.data', sep='\t', names=header)

user_num = ratings_data.user_id.unique().shape[0]
item_num = ratings_data.item_id.unique().shape[0]

train, test = cv.train_test_split(ratings_data, test_size=0.25)

#Create two user-item matrices, one for training and another for testing
train_matrix = np.zeros((user_num, item_num))
for line in train.itertuples():
    train_matrix[line[1]-1, line[2]-1] = line[3]

test_matrix = np.zeros((user_num, item_num))
for line in test.itertuples():
    test_matrix[line[1]-1, line[2]-1] = line[3]

def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    diffs = np.abs(prediction-ground_truth)
    mean = np.mean(diffs)
    std_dev = np.std(diffs)
    print("Mean: ", mean, "\nStd Dev: ", std_dev)
    return sqrt(mean_squared_error(prediction, ground_truth))

#get SVD components from train matrix. Choose k.
u, s, vt = svds(train_matrix, k=20)
s_diag_matrix = np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
print('User-based CF MSE: ' + str(rmse(X_pred, test_matrix)))
