# -*- coding: utf-8 -*-
"""01-Keras-CNN-MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kQWLakaMgXu_CNIbOWyMCkP75xGWOReq

<strong><center>Copyright by Pierian Data Inc.</center></strong> 
<strong><center>Created by Jose Marcial Portilla.</center></strong>
# Convolutional Neural Networks for Image Classification
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

"""##  Visualizing the Image Data"""

x_train.shape

single_image = x_train[0]

single_image

# 28x28 pixels
single_image.shape

plt.imshow(single_image, cmap='gray')
plt.show()

"""# PreProcessing Data

We first need to make sure the labels will be understandable by our CNN.

## Labels
"""

y_train

y_test

"""Our labels are literally categories of numbers. We need to translate this to be "one hot encoded" so our CNN can understand, otherwise it will think this is some sort of regression problem on a continuous axis. Keras has an easy to use function for this:"""

from tensorflow.keras.utils import to_categorical

y_example = to_categorical(y_train)

y_example

y_example.shape

y_example[0]

y_cat_test = to_categorical(y_test, 10)

y_cat_train = to_categorical(y_train, 10)

"""### Processing X Data

We should normalize the X data
"""

single_image.max()

single_image.min()

x_train = x_train/255
x_test = x_test/255

scaled_image = x_train[0]

scaled_image.max()

scaled_image.min()

scaled_image

plt.imshow(scaled_image, cmap='Purples')
plt.show()

"""## Reshaping the Data

Right now our data is 60,000 images stored in 28 by 28 pixel array formation. 

This is correct for a CNN, but we need to add one more dimension to show we're dealing with 1 RGB channel (since technically the images are in black and white, only showing values from 0-255 on a single channel), an color image would have 3 dimensions.
"""

x_train.shape

x_test.shape

"""Reshape to include channel dimension (in this case, 1 channel)"""

# batch_size, width, height, color_channels
x_train = x_train.reshape(60000,28,28,1)

# batch_size, width, height, color_channels
x_test = x_test.reshape(10000,28,28,1)

"""# Training the Model"""
