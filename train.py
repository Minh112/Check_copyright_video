import os

import numpy as np
from keras import Sequential
from keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.utils import shuffle

# HOME = os.getcwd()
# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)
#
# LOGGER = logging.getLogger("check_video.train")
# setup_loggers(LOG_DIR)
# logging.basicConfig(level=LOGLEVEL, format=FILE_LOG_FORMAT)


def build_model():
    model = Sequential()
    #model.add(LSTM(256, dropout=0.2))
    model.add(Dense(1024, activation='relu', input_shape=(None,2048)))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model


def train_model(file_other, file_true, file_weight):
    data_other = np.load(file_other)
    data_true = np.load(file_true)
    label_other = np.zeros(shape=len(data_other), dtype=int)
    label_true = np.ones(shape=len(data_true), dtype=int)

    X_train = np.concatenate((data_other, data_true))
    Y_train = np.concatenate((label_other, label_true))
    X_train, Y_train = shuffle(X_train, Y_train)
    model = build_model()
    #model.load_weights("Save_model/VGG16v1.h5")
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['acc'])
    train = model.fit(X_train, Y_train, steps_per_epoch=50, epochs=10, verbose=1)

    model.save_weights(file_weight)
    accuracy = train.history['acc'][-1]
    #LOGGER.info(f"Saved weights in 'Save_model/VGG16v1.h5'")

    return accuracy


if __name__ == '__main__':
    file_other = "npy/Other.npy"
    list_npy_true = os.listdir("npy")
    list_npy_true.remove("Other.npy")
    for npy_true in list_npy_true:
        file_true = os.path.join("npy", npy_true)
        file_weight = "weight/" + npy_true[:-4] + ".h5"
        accuracy = train_model(file_other, file_true, file_weight)
        print(accuracy)




