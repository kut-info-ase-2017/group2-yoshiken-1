
import sys
import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib

subjects = 2
dataset_path = '/Users/yoshilab/asd/test/learningtest/dataset/'
model_path = '/Users/yoshilab/asd/test/learningtest/models/'
FEATURE = 'AKAZE'
GRAYSCALE = 0
VW_DIM = 100
IMAGE_NUM = 200

# Keypoint Descriptor
def getkeypoint(img, feature):

    if feature == 'AKAZE':
        detector = cv2.AKAZE_create()
    elif feature == 'ORB':
        detector = cv2.ORB_create()
    else:
        print("detector not found")
        sys.exit(0)

    keypoints, descriptor = detector.detectAndCompute(img, None)
    out = cv2.drawKeypoints(img, keypoints, None)

    return keypoints, descriptor ,out

# Create Empty Array for append all images feature
def makeEmptyArray(feature):

    if feature == 'AKAZE':
        array = np.empty((0,61))
    elif feature == 'ORB':
        array = np.empty((0,32))
    else:
        print("detector not found")
        sys.exit(0)

    return array

def createBoF(features):

    kmeans = KMeans(n_clusters=VW_DIM, random_state=1, verbose=1, n_jobs=-1)

    model = kmeans.fit(features)

    joblib.dump(model, model_path + 'Bof.pkl')


if __name__ == '__main__':

    featureArray = makeEmptyArray(FEATURE)

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
                keypoints, descriptor, outimg = getkeypoint(img, FEATURE)

                if (descriptor is not None):
                    try:
                        if descriptor.shape[1]:
                            print(descriptor.shape)
                            featureArray = np.append(featureArray, descriptor,  axis=0)
                    except AttributeError:
                        print('1row')
                        featureArray = np.append(featureArray, [descriptor], axis=0)


                # print(descriptor.shape)
                # featureArray = np.append(featureArray, descriptor, axis=0)

                image_num += 1
                if(image_num == IMAGE_NUM): break

    createBoF(featureArray)
