from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

from keras.layers.core import Dense, Activation, Dropout, Flatten

from keras.layers.pooling import MaxPool2D
from keras.utils import np_utils

import os
import cv2
import numpy as np

img_rows, img_cols = 50, 150
img_channels = 3
nb_classes = 4
nb_epoch = 30
batch_size = 50

# Dataset
dataset_path = "./raspic/raspic/"

all_images = np.empty((0,img_rows,img_cols,3))
all_label = np.empty((0))

files = os.listdir(dataset_path)
subjects = [f for f in files if os.path.isdir(os.path.join(dataset_path, f))]

for subject in subjects:
    filelist = os.listdir(dataset_path + str(subject))
    print(str(subject) + '------------------------')

    for file in filelist:
        if file.endswith(".jpg"):
            print(str(file) + "*************")

            img = cv2.imread(dataset_path + str(subject) + '/' + str(file))
            print(img.shape)
            img = cv2.resize(img, (img_cols, img_rows))
            img = img / 255.0
            print(img.shape)
            img = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2]))
            print(img.shape)
            print(all_images.shape)
            all_images = np.append(all_images, img, axis=0)
            all_label = np.append(all_label, int(subject))

X_train = all_images
Y_train = np_utils.to_categorical(all_label, nb_classes)

model = Sequential()

# model.add(Conv2D(32, 3, input_shape=(32, 32, 3)))
model.add(Conv2D(32, 3, input_shape=(img_rows, img_cols, 3)))
model.add(Activation('relu'))
model.add(Conv2D(32,3))
model.add(Activation('relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(64, 3))
model.add(Activation('relu'))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(1024))
model.add(Activation('relu'))
model.add(Dropout(1.0))

model.add(Dense(nb_classes, activation='softmax'))

adam = Adam(lr=1e-4)

model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=["accuracy"])

# plot_model(model, to_file='./model2.png')
es_cb = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='auto')
history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=nb_epoch, verbose=1, validation_split=0.1, callbacks=[es_cb])
# Save model
model.save('./model/my_model.h5')


