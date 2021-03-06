# -*- coding: utf-8 -*-
"""class9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11_4a52b_I0SwfwJAhd3i7tFUsXBkQUDJ
"""

import zipfile
local_zip='/content/v_data.zip'
zip_ref=zipfile.ZipFile(local_zip,'r')
zip_ref.extractall()
zip_ref.close()

from keras.preprocessing.image import ImageDataGenerator 
from keras.models import Sequential 
from keras.layers import Conv2D, MaxPooling2D 
from keras.layers import Activation, Dropout, Flatten, Dense 
from keras import backend as K 
from tensorflow.keras import layers 
 
  
img_width, img_height = 224, 224

"""Train Data : Train data contains the 200 images of each cars and planes i.e. total their are 400 images in the training dataset

Test Data : Test data contains 50 images of each cars and planes i.e. total their are 100 images in the test dataset

Here, the train_data_dir is the train dataset directory. validation_data_dir is the directory for validation data. nb_train_samples is the total number train samples. nb_validation_samples is the total number of validation samples.
"""

train_data_dir = '/content/v_data/train'
validation_data_dir = '/content/v_data/test'
nb_train_samples = 400 
nb_validation_samples = 100
epochs = 10
batch_size = 16
  
if K.image_data_format() == 'channels_first': 
    input_shape = (3, img_width, img_height) 
else: 
    input_shape = (img_width, img_height, 3)

model = Sequential() 
model.add(Conv2D(32, (2, 2), input_shape = input_shape)) 
model.add(Activation('relu')) 
model.add(MaxPooling2D(pool_size =(2, 2))) 
  
model.add(Conv2D(32, (2, 2))) 
model.add(Activation('relu')) 
model.add(MaxPooling2D(pool_size =(2, 2))) 
  
model.add(Conv2D(64, (2, 2))) 
model.add(Activation('relu')) 
model.add(MaxPooling2D(pool_size =(2, 2))) 
  
model.add(Flatten()) 
model.add(Dense(64)) 
model.add(Activation('relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(1)) 
model.add(Activation('sigmoid'))

model.compile(loss ='binary_crossentropy', 
                     optimizer ='rmsprop', 
                   metrics =['accuracy'])

"""Image Augmentation"""

train_datagen = ImageDataGenerator( 
                rescale = 1. / 255, 
                 shear_range = 0.2, 
                  zoom_range = 0.2, 
            horizontal_flip = True) 
  
test_datagen = ImageDataGenerator(rescale = 1. / 255) 
  
train_generator = train_datagen.flow_from_directory(train_data_dir, 
                              target_size =(img_width, img_height), 
                     batch_size = batch_size, class_mode ='binary') 
  
validation_generator = test_datagen.flow_from_directory( 
                                    validation_data_dir, 
                   target_size =(img_width, img_height), 
          batch_size = batch_size, class_mode ='binary')

"""validation accuracy=88% using simple CNN model"""

model.fit_generator(train_generator, 
    steps_per_epoch = nb_train_samples // batch_size, 
    epochs = epochs, validation_data = validation_generator, 
    validation_steps = nb_validation_samples // batch_size) 
  
model.save_weights('model_saved.h5')

"""Transfer Learning
1. Very Deep Convolutional Networks for Large-Scale Image Recognition(VGG-16)

The VGG-16 is one of the most popular pre-trained models for image classification. Introduced in the famous ILSVRC 2014 Conference, it was and remains THE model to beat even today. Developed at the Visual Graphics Group at the University of Oxford, VGG-16 beat the then standard of AlexNet and was quickly adopted by researchers and the industry for their image Classification Tasks.
"""

from tensorflow.keras.applications.vgg16 import VGG16

base_model = VGG16(input_shape = (224, 224, 3), # Shape of our images
include_top = False, # Leave out the last fully connected layer
weights = 'imagenet')

"""Loading the Base Model

We will be using only the basic models, with changes made only to the final layer. This is because this is just a binary classification problem while these models are built to handle up to 1000 classes.
Since we don’t have to train all the layers, we make them non_trainable:
"""

for layer in base_model.layers:
    layer.trainable = False

"""Compile and Fit

We will then build the last fully-connected layer. I have just used the basic settings, but feel free to experiment with different values of dropout, and different Optimisers and activation functions.
"""

x = layers.Flatten()(base_model.output)

# Add a fully connected layer with 512 hidden units and ReLU activation
x = layers.Dense(512, activation='relu')(x)

# Add a dropout rate of 0.5
x = layers.Dropout(0.5)(x)

# Add a final sigmoid layer for classification
x = layers.Dense(1, activation='sigmoid')(x)

model = tf.keras.models.Model(base_model.input, x)

model.compile(optimizer = tf.keras.optimizers.RMSprop(lr=0.0001), loss = 'binary_crossentropy',metrics = ['acc'])

vgghist = model.fit(train_generator, validation_data = validation_generator, steps_per_epoch = 25, epochs = 2)

"""We were able to achieve a validation Accuracy of 98% with just 2 epochs and without any major changes to the model. This is where we realize how powerful transfer learning is and how useful pre-trained models for image classification can be. A caveat here though – VGG16 takes up a long time to train compared to other models and this can be a disadvantage when we are dealing with huge datasets.

USEFUL SOURCES/WEBSITES:

1.GEEKS FOR GEEKS

2.ANALYTICS VIDHYA

3.KAGGLE

4.MEDIUM
"""