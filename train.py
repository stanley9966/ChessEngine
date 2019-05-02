import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, Flatten

class ProcessedDataLoader:
    def __init__(self):
        data = np.load("processed_games.npz")
        self.X = data['arr_0']
        self.Y = data['arr_1']
        print("loaded", self.X.shape, self.Y.shape) # (5,8,8) only 1024 samples right now

if __name__ == "__main__":
    loader = ProcessedDataLoader()
    #create model
    model = Sequential()
    # Layers
    model.add(Conv2D(16, kernel_size=3, activation='relu', input_shape=(5,8,8)))
    model.add(Conv2D(32, kernel_size=3, activation='relu'))

    model.add(Flatten())
    model.add(Dense(1, activation='tanh'))
    # compile model
    model.compile(optimizer='adam', loss='mean_squared_error')
    # train the model
    X_train = loader.X 
    y_train = loader.Y
    batch_size = 256
    num_epochs = 100 
    model.fit(X_train, y_train, epochs=num_epochs, steps_per_epoch = batch_size)
    model.save('saved_model.h5')
