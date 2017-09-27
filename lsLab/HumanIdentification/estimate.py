from keras.models import load_model

import cv2
import numpy as np
import pandas as pd
import sys
import subprocess
# load csv
argvs = sys.argv
argc = len(argvs)
if (argc != 2):
    print("Usage:" + argvs[0])
    quit()

target_file = argvs[1]

name_list = ['RYONAI', 'ZHUO', 'NAKAYAMA', 'SASATANI']

# load model
model = load_model('./model/my_model.h5')

img_rows, img_cols = 50, 150 
img_channels = 3
nb_classes = 3
nb_epoch = 30
batch_size = 50

# load filename, in/out
testdata_path = './cropped_images/' + str(target_file)
inout = target_file[:3]
sys.exit(0)

# read img file
img = cv2.imread(testdata_path)
img = cv2.resize(img, (img_cols, img_rows))
img = img / 255.0
img = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2]))

# predict
test_p = model.predict([img])
test_class = model.predict_classes([img])
print(test_class)
print(test_p[0][test_class[0]])
print(name_list[test_class[0]])

###target_file['0'][0] = name_list[test_class[0]]

# json file update
cmd = "python3"
tar = "/opt/lampp/htdocs/phpapi/write.py"
arg1 = str(name_list[test_class[0]])
arg2 = str(inout)
print(cmd)
res = subprocess.call([cmd, tar , arg1, arg2])
