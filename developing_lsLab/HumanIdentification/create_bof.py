
import cv2
import numpy as np
import sys
import os
import csv
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.externals import joblib


from create_model import getkeypoint

subjects = 2
dataset_path = '/Users/yoshilab/asd/test/learningtest/dataset/'
model_path = '/Users/yoshilab/asd/test/learningtest/models/'
FEATURE = 'AKAZE'
GRAYSCALE = 0
VW_DIM = 100
IMAGE_NUM = 200


def makeVW(model, img):

    vw_list = []

    keypoints, descriptions, outimg = getkeypoint(img, FEATURE)

    if (descriptions is not None):
        try:
            if descriptions.shape[1]:

                for description in descriptions:
                    vw_label = model.predict([description])
                    vw_list.append(vw_label)

        except AttributeError:
            vw_label = model.predict([descriptions])
            vw_list.append(vw_label)
            
    # for description in descriptions:
    #     vw_label = model.predict([description])
    #     vw_list.append(vw_label)

    hist, trash = np.histogram(vw_list, bins=VW_DIM, range=(0, VW_DIM-1))

    return hist


if __name__ == '__main__':

    model = joblib.load('./models/Bof.pkl')

    files = os.listdir(dataset_path)
    subjects = [f for f in files if os.path.isdir(os.path.join(dataset_path, f))]

    for subject in subjects:
        filelist = os.listdir(dataset_path + str(subject))
        print(str(subject) + '------------------------')

        image_num = 0
        for file in filelist:
            print(str(file) + "*************")
            if file.endswith(".jpg"):

                img = cv2.imread(dataset_path + str(subject) + '/' + str(file), GRAYSCALE)

                vw_hist = pd.Series(makeVW(model, img))

                csvname, ext = os.path.splitext(file) 

                vw_hist.to_csv('./vw/' + str(subject) + '/' + str(csvname) + '.csv', index=False)

                image_num += 1
                if (image_num == IMAGE_NUM): break

                # with open('./vw/' + str(subject) + '/' + str(csvname) + '.csv') as x:
                #     writer = csv.writer(x, lineterminator='\n')
                #     writer.writerow(vw_hist)
