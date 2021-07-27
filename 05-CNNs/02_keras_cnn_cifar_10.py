# -*- coding: utf-8 -*-
"""02-Keras-CNN-CIFAR-10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zvSY4sAhUTj5r40IdTmJljD2u7ChHyv-

# CIFAR-10 Multiple Classes

Let's go over another example of using Keras and building out CNNs. This time will use another famous data set, the CIFAR-10 dataset which consists of 10 different image types.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""# The Data

CIFAR-10 is a dataset of 50,000 32x32 color training images, labeled over 10 categories, and 10,000 test images.

Label	Description:
* 0	airplane
* 1	automobile
* 2	bird
* 3	cat
* 4	deer
* 5	dog
* 6	frog
* 7	horse
* 8	ship
* 9	truck
"""

from tensorflow.keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train.shape

x_train[0].shape

# frog
plt.figure(figsize = (1,1))
plt.imshow(x_train[0])
plt.show()

# HORSE
plt.figure(figsize = (1,1))
plt.imshow(x_train[12])
plt.show()

"""# PreProcessing"""

x_train[0]

x_train.max()

x_train.min()

x_train = x_train/255
x_test = x_test/255

x_test.shape

x_train.max()

"""## Labels"""

from tensorflow.keras.utils import to_categorical

y_test

y_test.shape

y_cat_test = to_categorical(y_test, 10)

y_cat_test.shape

y_cat_train = to_categorical(y_train, 10)

y_train[0]

y_cat_train[0]

"""----------
# Building the Model
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense

model = Sequential()

## FIRST SET OF LAYERS

# CONVOLUTIONAL LAYER
model.add(Conv2D(filters=32, kernel_size=(4,4), input_shape=(32,32,3), activation='relu'))
# POOLING LAYER
model.add(MaxPool2D(pool_size=(2,2)))

## SECOND SET OF LAYERS

# CONVOLUTIONAL LAYER
model.add(Conv2D(filters=32, kernel_size=(4,4), input_shape=(32,32,3), activation='relu'))
# POOLING LAYER
model.add(MaxPool2D(pool_size=(2,2)))

# FLATTEN IMAGES FROM 32 by 32 by 3 to 3,072 BEFORE FINAL LAYER
model.add(Flatten())

# 256 NEURONS IN DENSE HIDDEN LAYER (YOU CAN CHANGE THIS NUMBER OF NEURONS)
model.add(Dense(256, activation='relu'))

# LAST LAYER IS THE CLASSIFIER, THUS 10 POSSIBLE CLASSES
model.add(Dense(10, activation='softmax'))

# COMPILING THE MODEL
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(monitor='val_loss', patience=3)

model.fit(x_train, y_cat_train, epochs=15, validation_data=(x_test, y_cat_test), callbacks=[early_stop])

"""## Evaluate the Model"""

metrics = pd.DataFrame(model.history.history)

metrics

metrics[['accuracy', 'val_accuracy']].plot()
plt.show()

metrics[['loss', 'val_loss']].plot()
plt.show()

print(model.metrics_names)
print(model.evaluate(x_test,y_cat_test,verbose=0))

print(model.metrics_names)
print(model.evaluate(x_train,y_cat_train,verbose=0))

from sklearn.metrics import classification_report, confusion_matrix

predictions = model.predict_classes(x_test)

predictions_2 = np.argmax(model.predict(x_test), axis=-1)

print(classification_report(y_test, predictions))

print(classification_report(y_test, predictions_2))

print(confusion_matrix(y_test,predictions))

import seaborn as sns
plt.figure(figsize=(10,6))
sns.heatmap(confusion_matrix(y_test,predictions),annot=True)
plt.show()

"""# Predicting a given image"""

my_image = x_test[16]

plt.figure(figsize=(1,1))
plt.imshow(my_image)
plt.show()

# SHAPE --> (num_images,width,height,color_channels)
print(np.argmax(model.predict(my_image.reshape(1,32,32,3)), axis=-1))

print(y_test[16])

"""5 is dog.

## Saving the Model
"""

model.save('cifar10_10epochs.h5')