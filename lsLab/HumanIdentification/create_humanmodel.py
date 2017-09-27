
import cv2
import numpy as np
import sys
import os
import csv
import pandas as pd

from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import metrics

from create_model import getkeypoint

subjects = 2
dataset_path = '/Users/yoshilab/asd/test/learningtest/vw/'
model_path = '/Users/yoshilab/asd/test/learning/models/'
FEATURE = 'AKAZE'
GRAYSCALE = 0
VW_DIM = 100



if __name__ == '__main__':

    # all_descripiton = np.empty((0,VW_DIM))
    # all_label = np.empty(0)
    all_descripiton = pd.DataFrame([])
    all_label = pd.DataFrame([])


    files = os.listdir(dataset_path)
    subjects = [f for f in files if os.path.isdir(os.path.join(dataset_path, f))]

 
    for subject in subjects:
        filelist = os.listdir(dataset_path + str(subject))
        print(str(subject) + '------------------------')

        for file in filelist:
            if file.endswith(".csv"):
                print(str(file) + "*************")

                vw_histogram = pd.DataFrame([pd.read_csv('./vw/' + str(subject) + '/' + str(file), header=None)][0]).T
                all_descripiton = pd.DataFrame.append(all_descripiton, vw_histogram)
                all_label = pd.DataFrame.append(all_label, [pd.Series(int(subject))])


    train_data, test_data, train_label, test_label = train_test_split(all_descripiton, all_label.values.flatten(), test_size=0.33)

    # clf = SVC()

    clf = MLPClassifier(hidden_layer_sizes=(300, 200, 100), random_state=1, activation='relu')

    # clf.fit(all_descripiton, all_label.values.flatten())
    clf.fit(train_data, train_label)

    predicted = clf.predict(test_data)

    print(metrics.confusion_matrix(predicted, test_label))
    print(metrics.classification_report(predicted, test_label))

