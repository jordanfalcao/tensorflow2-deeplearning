# -*- coding: utf-8 -*-
"""02-DCGANS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G-clrn853fn5pHT0PBvMJfiFx_TwRwUx

# GANs - Generative Adverserial Networks
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()

plt.imshow(X_train[0])
plt.show()

y_train

"""## Reshape and Rescale Images for DCGAN

Generator will use tanh activation function for the last layer, so we want to reshape X_train to be within -1 to 1 limits.
"""

X_train = X_train/255

X_train = X_train.reshape(-1, 28, 28, 1) * 2. - 1.

X_train.min()

X_train.max()

"""## Filtering out the Data for Faster Training on Smaller Dataset"""

only_zeros = X_train[y_train==0]

only_zeros.shape

import tensorflow as tf
from tensorflow.keras.layers import Dense,Reshape,Dropout,LeakyReLU,Flatten,BatchNormalization,Conv2D,Conv2DTranspose
from tensorflow.keras.models import Sequential

np.random.seed(42)
tf.random.set_seed(42)

codings_size = 100

generator = Sequential()

generator.add(Dense(7 * 7 * 128, input_shape=[codings_size]))
generator.add(Reshape([7, 7, 128]))
generator.add(BatchNormalization())
generator.add(Conv2DTranspose(64, kernel_size=5, strides=2, padding="same",
                                 activation="relu"))
generator.add(BatchNormalization())

generator.add(Conv2DTranspose(1, kernel_size=5, strides=2, padding="same",
                                 activation="tanh"))

discriminator = Sequential()

discriminator.add(Conv2D(64, kernel_size=5, strides=2, padding="same",
                        activation=LeakyReLU(0.3),
                        input_shape=[28, 28, 1]))
discriminator.add(Dropout(0.5))
discriminator.add(Conv2D(128, kernel_size=5, strides=2, padding="same",
                        activation=LeakyReLU(0.3)))
discriminator.add(Dropout(0.5))
discriminator.add(Flatten())
# sigmoid - 0 or 1
discriminator.add(Dense(1, activation="sigmoid"))

GAN = Sequential([generator, discriminator])

discriminator.compile(loss="binary_crossentropy", optimizer="adam")
discriminator.trainable = False

GAN.compile(loss="binary_crossentropy", optimizer="adam")

GAN.layers

GAN.summary()

# generator
GAN.layers[0].summary()

# discriminator
GAN.layers[1].summary()

"""### Setting up Training Batches"""

batch_size = 32

"""https://stackoverflow.com/questions/46444018/meaning-of-buffer-size-in-dataset-map-dataset-prefetch-and-dataset-shuffle

The buffer_size in Dataset.shuffle() can affect the randomness of your dataset, and hence the order in which elements are produced. 
"""

# my_data = X_train
my_data = only_zeros

dataset = tf.data.Dataset.from_tensor_slices(my_data).shuffle(buffer_size=1000)

type(dataset)

dataset = dataset.batch(batch_size, drop_remainder=True).prefetch(1)

epochs = 20

"""**NOTE: The generator never actually sees any real images. It learns by viewing the gradients going back through the discriminator. The better the discrimnator gets through training, the more information the discriminator contains in its gradients, which means the generator can being to make progress in learning how to generate fake images, in our case, fake zeros.**

## Training Loop
"""

# Grab the seprate components
generator, discriminator = GAN.layers

# For every epcoh
for epoch in range(epochs):
    print(f"Currently on Epoch {epoch+1}")
    i = 0
    # For every batch in the dataset
    for X_batch in dataset:
        i=i+1
        if i%20 == 0:
            print(f"\tCurrently on batch number {i} of {len(my_data)//batch_size}")
        #####################################
        ## TRAINING THE DISCRIMINATOR ######
        ###################################
        
        # Create Noise
        noise = tf.random.normal(shape=[batch_size, codings_size])
        
        # Generate numbers based just on noise input
        gen_images = generator(noise)
        
        # Concatenate Generated Images against the Real Ones
        # TO use tf.concat, the data types must match!
        X_fake_vs_real = tf.concat([gen_images, tf.dtypes.cast(X_batch,tf.float32)], axis=0)
        
        # Targets set to zero for fake images and 1 for real images
        y1 = tf.constant([[0.]] * batch_size + [[1.]] * batch_size)
        
        # This gets rid of a Keras warning
        discriminator.trainable = True
        
        # Train the discriminator on this batch
        discriminator.train_on_batch(X_fake_vs_real, y1)
        
        
        #####################################
        ## TRAINING THE GENERATOR     ######
        ###################################
        
        # Create some noise
        noise = tf.random.normal(shape=[batch_size, codings_size])
        
        # We want discriminator to belive that fake images are real
        y2 = tf.constant([[1.]] * batch_size)
        
        # Avois a warning
        discriminator.trainable = False
        
        GAN.train_on_batch(noise, y2)
        
print("TRAINING COMPLETE")

noise = tf.random.normal(shape=[10, codings_size])

noise.shape

noise.shape

plt.imshow(noise)
plt.show()

images = generator(noise)

for image in images:
    plt.imshow(image.numpy().reshape(28,28))
    plt.show()

"""## Saving models:"""

generator.save('mnist_GAN-CNN_generator.h5')

discriminator.save('mnist_GAN-CNN_discriminator.h5')

GAN.save('mnist_GAN-CNN_model.h5')