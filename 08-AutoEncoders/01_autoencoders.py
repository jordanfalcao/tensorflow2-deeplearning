# -*- coding: utf-8 -*-
"""01-Autoencoders.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XZSt_ctNMlzgZfTVU4gdmFApnsisbyWz

# AutoEncoders for Dimensionality Reduction
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# enerate isotropic Gaussian blobs for clustering
from sklearn.datasets import make_blobs

data = make_blobs(n_samples=300,
    n_features=2,
    centers=2,       # 2 clusters
    cluster_std=1.0,random_state=101)

# data

X,y = data

y

X.shape

# third feature, just noise
np.random.seed(seed=101)
z_noise = np.random.normal(size=len(X))
z_noise = pd.Series(z_noise)

z_noise

feat = pd.DataFrame(X)
feat.head()

feat = pd.concat([feat,z_noise],axis=1)
feat.columns = ['X1','X2','X3']

feat.head()

# 2 visible clusters
plt.figure(figsize=(8,5))
plt.scatter(feat['X1'],feat['X2'],c=y)
plt.show()

"""https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#scatter-plots"""

from mpl_toolkits.mplot3d import Axes3D

# %matplotlib notebook

# third dimension, only noise
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(feat['X1'], feat['X2'], feat['X3'], c=y)

"""# Encoder and Decoder"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD  # stochastic gradient descent

# 3 --> 2
encoder = Sequential()
encoder.add(Dense(units=2,activation='relu',input_shape=[3]))

# 2 ---> 3
decoder = Sequential()
decoder.add(Dense(units=3,activation='relu',input_shape=[2]))

# ENCODER
# 3 ---> 2 ----> 3
autoencoder = Sequential([encoder,decoder])  # list

autoencoder.compile(loss="mse" ,optimizer=SGD(learning_rate=1.5))

"""## Scaler"""

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# Note how all the data is used! There is no "right" answer here
# so we don't split the data
scaled_data = scaler.fit_transform(feat)

"""## Fit the model"""

autoencoder.fit(scaled_data,scaled_data,epochs=5)

# just the ENCODER: 3 ---> 2
encoded_2dim = encoder.predict(scaled_data)

encoded_2dim

scaled_data.shape

# 3 ---> 2
encoded_2dim.shape

plt.scatter(encoded_2dim[:,0],encoded_2dim[:,1],c=y)
plt.show()