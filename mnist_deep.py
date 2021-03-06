'''Train a simple convnet on the MNIST dataset.

Run on GPU: THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python mnist_shallow.py

Get to % test accuracy after 12 epochs (there is still a lot of margin for parameter tuning).
? seconds per epoch on CPU.
'''

from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.utils import np_utils

batch_size = 128
nb_classes = 10
nb_epoch = 30

# the data, shuffled and split between tran and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()
model.add(Dense(100, init='uniform', input_shape=(784,)))
model.add(Activation('sigmoid'))
model.add(Dense(10, init='uniform', input_shape=(100,)))
model.add(Activation('softmax'))

model.compile(loss='mse', optimizer='sgd', metrics=['accuracy'])

hist = model.fit(X_train, Y_train, batch_size=batch_size, 
                 nb_epoch=nb_epoch, 
                 verbose=1, validation_split=0.2)

score = model.evaluate(X_test, Y_test, verbose=0)

print('Test score:', score[0])
print('Test accuracy:', score[1])
