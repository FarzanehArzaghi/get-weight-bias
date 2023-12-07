# -*- coding: utf-8 -*-
"""MyModel70_MNIST012.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ctUiLc2z0GAmV2s8Yoi6vGlD3sCj_Dsc
"""

!pip install keras.utils

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import numpy
from tensorflow.keras.utils import plot_model

###laod dataset
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

####seprate 0,1,2 from MNIST dataset in train and test data with their labels

train_012_list = []
test_012_list =[]
tr_label_012_list = []
te_label_012_list=[]
counter1_1 = -1
counter1_2 = -1
for i in range(0, 60000-1):
    if (train_labels[i]== 0 or train_labels[i]==1 or train_labels[i]==2):
        counter1_1 = counter1_1+1
        train_012_list.insert(counter1_1,train_images[i])
        tr_label_012_list.insert(counter1_1,train_labels[i])
for j in range (0, 10000-1):
     if (test_labels[j]== 0 or test_labels[j]==1 or test_labels[j]==2):
        counter1_2 = counter1_2 +1
        test_012_list.insert(counter1_2,test_images[j])
        te_label_012_list.insert(counter1_2,test_labels[j])

train_012_array = numpy.array(train_012_list)
test_012_array = numpy.array(test_012_list)
tr_label_012_array = numpy.array(tr_label_012_list)
te_label_012_array = numpy.array(te_label_012_list)

##### checking the correct of separation of 0,1,2
print(train_012_list[0])

### checking 0,1,2 dataset's attributes
print(train_012_array.ndim)
print(train_012_array.shape)
print(train_012_array.dtype)

#MyModel
model = keras.models.Sequential([
    keras.layers.Conv2D(filters=10, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same", input_shape=(28,28,1)),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    keras.layers.Conv2D(filters=15, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    keras.layers.Conv2D(filters=20, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(70, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(70, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(3, activation='softmax')
])

#### model compile
model.compile(loss='sparse_categorical_crossentropy' , optimizer=tf.optimizers.SGD(learning_rate=0.001), metrics=['accuracy'])
model.summary()

plot_model(model, to_file='modelstructure.pdf')

#### model training
model.fit(train_012_array,tr_label_012_array, batch_size=128, epochs=200)

### testing the trained model
test_loss, test_acc = model.evaluate(test_012_array, te_label_012_array)

#### loss & acc
print(test_loss)
print(test_acc)

### checking the layers' name
model.layers[6].name

####conv2d_0 layer
layer0_weights=[]
layer0_bias=[]
count=0
layer0_weights.insert(count, model.layers[0].get_weights()[0])
layer0_bias.insert(count, model.layers[0].get_weights()[1])

####conv2d_1 layer
layer3_weights=[]
layer3_bias=[]
count=0
layer3_weights.insert(count, model.layers[3].get_weights()[0])
layer3_bias.insert(count, model.layers[3].get_weights()[1])

####conv2d_2 layer
layer6_weights=[]
layer6_bias=[]
count=0
layer6_weights.insert(count, model.layers[6].get_weights()[0])
layer6_bias.insert(count, model.layers[6].get_weights()[1])

#### checking conv2d_0 layer weights & biases
model.layers[0].get_weights()
print(layer0_weights)
print(layer0_bias)

####saving conv2d_0's Weight & Bias for python loading
with open("conv2d0_W&B.txt", "w") as output:
         output.write(str(model.layers[0].get_weights()[:]))
with open("conv2d0_W.txt", "w") as output:
         output.write(str(layer0_weights))
with open("conv2d0_B.txt", "w") as output:
         output.write(str(layer0_bias))

####saving conv2d_1's Bias for python loading
with open("conv2d1_B.txt", "w") as output:
         output.write(str(layer3_bias))

####saving conv2d_2's Bias for python loading
with open("conv2d2_B.txt", "w") as output:
         output.write(str(layer6_bias))

######saving conv2d_0' kernels for VHDL loading
kernels_conv2d0=[]
for i in range (0, 10):
    kernels_conv2d0.insert(i,model.layers[0].get_weights()[0][:,:,:,i])
    print("kernel",i,"=",model.layers[0].get_weights()[0][:,:,:,i],"\n")

######changing conv2d_1' kernels for VHDL loading
kernels_conv2d1=[]
for i in range (0, 15):
    for j in range(0, 10):
          kernels_conv2d1.insert(i,model.layers[3].get_weights()[0][:,:,j,i])
          print("kernel",i,"=",model.layers[3].get_weights()[0][:,:,j,i],"\n")

######changing conv2d_2' kernels for VHDL loading
kernels_conv2d2=[]
for i in range (0, 20):
    for j in range(0, 15):
          kernels_conv2d2.insert(i,model.layers[6].get_weights()[0][:,:,j,i])
          print("kernel",i,"=",model.layers[6].get_weights()[0][:,:,j,i],"\n")

#### checking kernels' shape and contents
print(model.layers[6].get_weights()[0].shape)
print (model.layers[3].get_weights()[0][:,:,1,0])

####saving conv2d_1' kernels in txt file for VHDL loading
with open("conv2d1_kernels.txt", "w") as output:
         output.write(str(kernels_conv2d1))

####saving conv2d_2' kernels in txt file for VHDL loading
with open("conv2d2_kernels.txt", "w") as output:
         output.write(str(kernels_conv2d2))

##### get & save BN layer weight & biases for laoding on python
print(model.layers[1].get_weights(),"\n")
print(model.layers[4].get_weights(),"\n")
print(model.layers[7].get_weights(),"\n")
with open("BN1.txt", "w") as output:
         output.write(str(model.layers[1].get_weights()))
with open("BN4.txt", "w") as output:
         output.write(str(model.layers[4].get_weights()))
with open("BN7.txt", "w") as output:
         output.write(str(model.layers[7].get_weights()))

###saving model weight & biases in h5file
model.save_weights('MNIST012_trainfullnetwork.h5')

