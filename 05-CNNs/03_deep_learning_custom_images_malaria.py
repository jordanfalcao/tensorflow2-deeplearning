# -*- coding: utf-8 -*-
"""03-Deep-Learning-Custom-Images-Malaria.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CYvCf3JbVXadqcxHqbCpyHWku10x_qGC

# Working with Custom Images

Let's explore what its like to work with a more realistic data set.

## The Data

----------
--------

ORIGINAL DATA SOURCE:

The dataset contains 2 folders - Infected - Uninfected

And a total of 27,558 images.

Acknowledgements
This Dataset is taken from the official NIH Website: https://ceb.nlm.nih.gov/repositories/malaria-datasets/ 

**Note: We will be dealing with real image files, NOT numpy arrays. Which means a large part of this process will be learning how to work with and deal with large groups of image files. This is too much data to fit in memory as a numpy array, so we'll need to feed it into our model in batches.**

### Visualizing the Data


-------
Let's take a closer look at the data.
"""

# zip_path = base/’size_test/cats_dogs.zip’
# !cp “{zip_path}” .
# !unzip -q cats_dogs.zip
# !rm cats_dogs.zip

#  mounts the Google drive
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.image import imread

import zipfile
import os

# drive path
zip_path = '/content/drive/MyDrive/cell_images.rar'

# copying the file from drive to colab
!cp "{zip_path}" .

# unrar the file
!unrar x cell_images.rar

#!unrar x "/content/drive/MyDrive/cell_images.rar" "/content/drive/MyDrive/Tensorflow"

my_data_dir = '/content/cell_images'

# CONFIRM THAT THIS REPORTS BACK 'test', and 'train'
os.listdir(my_data_dir)

test_path = my_data_dir+'/test'
train_path = my_data_dir+'/train'

os.listdir(test_path)

os.listdir(train_path)

"""**Let's check how many images there are.**"""

len(os.listdir('/content/cell_images/test/parasitized'))

len(os.listdir('/content/cell_images/test/uninfected'))

len(os.listdir('/content/cell_images/train/parasitized'))

len(os.listdir('/content/cell_images/train/uninfected'))

"""**Single image.**"""

os.listdir(train_path+'/parasitized')[0]

para_cell = train_path+'/parasitized'+'/C100P61ThinF_IMG_20150918_144104_cell_162.png'

para_img = imread(para_cell)

plt.imshow(para_img)
plt.show()

os.listdir(train_path+'/uninfected')[0]

unifected_cell_path = train_path+'/uninfected/'+'/C145P106ThinF_IMG_20151016_154719_cell_57.png'
unifected_cell = imread(unifected_cell_path)
plt.imshow(unifected_cell)
plt.show()

"""**The images have differents dimensions. Let's find out the average dimensions of these images.**"""

para_img.shape

unifected_cell.shape

# Other options: https://stackoverflow.com/questions/1507084/how-to-check-dimensions-of-all-images-in-a-directory-using-python
 dim1 = []
 dim2 = []

 for image_filename in os.listdir(test_path+'/uninfected'):

   img = imread(test_path+'/uninfected/'+image_filename)
   d1, d2, colors_channel = img.shape
   dim1.append(d1)
   dim2.append(d2)

sns.jointplot(x= dim1, y = dim2)
plt.show()

# width pixel mean
np.mean(dim1)

# height pixel mean
np.mean(dim2)

# setting the average image dimension
image_shape = (130,130,3)

"""## Preparing the Data for the model

There is too much data for us to read all at once in memory. We can use some built in functions in Keras to automatically process the data, generate a flow of batches from a directory, and also manipulate the images.

### Image Manipulation

Its usually a good idea to manipulate the images with rotation, resizing, and scaling so the model becomes more robust to different images that our data set doesn't have. We can use the **ImageDataGenerator** to do this automatically for us. Check out the documentation for a full list of all the parameters you can use here!
"""

para_img.max()

unifected_cell.max()

unifected_cell.min()

para_img.min()

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# many way to change the images
help(ImageDataGenerator)

image_gen = ImageDataGenerator(rotation_range=20, # rotate the image 20 degrees
                               width_shift_range=0.10, # Shift the pic width by a max of 5%
                               height_shift_range=0.10, # Shift the pic height by a max of 5%
                               #rescale=1/255, # our data is already scaled.
                               shear_range=0.1, # Shear means cutting away part of the image (max 10%)
                               zoom_range=0.1, # Zoom in by 10% max
                               horizontal_flip=True, # Allo horizontal flipping
                               fill_mode='nearest' # Fill in missing pixels with the nearest filled value
                              )

plt.imshow(para_img)
plt.show()

# randomly transforming the image
plt.imshow(image_gen.random_transform(para_img))
plt.show()

# randomly transforming the image
plt.imshow(image_gen.random_transform(para_img))
plt.show()

"""### Generating many manipulated images from a directory


In order to use .flow_from_directory, you must organize the images in sub-directories. This is an absolute requirement, otherwise the method won't work. The directories should only contain images of one class, so one folder per class of images.

Structure Needed:

* Image Data Folder
    * Class 1
        * 0.jpg
        * 1.jpg
        * ...
    * Class 2
        * 0.jpg
        * 1.jpg
        * ...
    * ...
    * Class n
"""

# our data is separated in 2 directories
image_gen.flow_from_directory(train_path)

# our data is separated in 2 directories
image_gen.flow_from_directory(test_path)

"""# Creating the Model"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D

#https://stats.stackexchange.com/questions/148139/rules-for-selecting-convolutional-neural-network-hyperparameters
model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3,3),input_shape=image_shape, activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=image_shape, activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=image_shape, activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Flatten())


model.add(Dense(128))
model.add(Activation('relu'))

# Dropouts help reduce overfitting by randomly turning neurons off during training.
# Here we say randomly turn off 50% of neurons.
model.add(Dropout(0.5))

# Last layer, remember its binary so we use sigmoid
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

"""## Early Stopping"""

from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(monitor='val_loss',patience=2)

"""## Training the Model"""

batch_size = 16

image_shape[:2]

train_image_gen = image_gen.flow_from_directory(train_path,
                                                target_size=image_shape[:2],
                                                color_mode='rgb',
                                                batch_size=batch_size,
                                                class_mode='binary')

test_image_gen = image_gen.flow_from_directory(test_path,
                                                target_size=image_shape[:2],
                                                color_mode='rgb',
                                                batch_size=batch_size,
                                                class_mode='binary',
                                               shuffle=False)

train_image_gen.class_indices

test_image_gen.class_indices

# results = model.fit_generator(train_image_gen, epochs=20,
#                               validation_data=test_image_gen,
#                               callbacks=[early_stop])

from tensorflow.keras.models import load_model

# model.save('my_malaria_detector.h5')

# loading created model
model = load_model('my_malaria_detector.h5')

"""# Evaluating the Model"""

# losses = pd.DataFrame(model.history.history)

losses[['loss','val_loss']].plot()

model.metrics_names

model.evaluate_generator(test_image_gen)

# https://datascience.stackexchange.com/questions/13894/how-to-get-predictions-with-predict-generator-on-streaming-test-data-in-keras
pred_probabilities = model.predict_generator(test_image_gen)

pred_test = model.predict(test_image_gen)

pred_probabilities

test_image_gen.classes

# this value must be discussed with a specialist
predictions = pred_probabilities > 0.5

predictions

from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(test_image_gen.classes, predictions))

confusion_matrix(test_image_gen.classes, predictions)

"""# Predicting on an Image"""

from tensorflow.keras.preprocessing import image

para_cell

my_image = image.load_img(para_cell, target_size=image_shape)

my_image

type(my_image)

my_image = image.img_to_array(my_image)

my_image

type(my_image)

my_image.shape

# need to add batch to call in the model
my_image = np.expand_dims(my_image, axis = 0)

my_image.shape

# almost 0
model.predict(my_image)

test_image_gen.class_indices