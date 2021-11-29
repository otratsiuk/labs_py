import math
import matplotlib.pyplot as plt

class Dataset:
    dt_splitter = 2 / 3

    def __init__(self, dt_size, function):
        self.dt_size = dt_size
        self.func = function

        self.training_dt_size = round(self.dt_size * self.dt_splitter)
        self.validation_dt_size = self.dt_size - self.training_dt_size

        self.x = []
        self.y = []
        for _ in range(dt_size):
            self.x.append(_)
            self.y.append(self.func(_))


    def training_sample(self):
        return self.x[: self.training_dt_size], self.y[: self.training_dt_size]

    def validation_sample(self):
        return self.x[self.training_dt_size :], self.y[self.training_dt_size :]    

    #returns a list of samples formed by sliding window
    #takes set as list and splits it to samples of k elements
    def sliding_window_samples(self, set, k):
        samples = []
        for i in range(len(set) - k + 1):
            temp = []
            for j in range(k):
                temp.append(set[i + j])
            samples.append(temp)

        return samples            

    def sliding_window_e(self, set, k):
        return set[k :]