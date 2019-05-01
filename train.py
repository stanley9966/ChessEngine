import numpy as np

class ProcessedDataLoader:
    # Hotz imports torch Dataset
    def __init__(self):
        data = np.load("processed_games.npz")
        self.X = data['arr_0']
        self.Y = data['arr_1']
        print("loaded", self.X.shape, self.Y.shape)

if __name__ == "__main__":
    loader = ProcessedDataLoader()
