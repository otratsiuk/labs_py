import math
import matplotlib.pyplot as plt
import numpy as np
import csv

class Dataset:
    dt_splitter = 2 / 3

    def __init__(self, dt_size, function):
        self.dt_size = dt_size
        self.func = function

        self.training_dt_size = round(self.dt_size * self.dt_splitter)
        self.validation_dt_size = self.dt_size - self.training_dt_size

        self.x = np.linspace(-10, 10, self.dt_size)
        self.y = []
        for x in self.x:
            self.y.append(self.func(x))    

    def training_sample(self):
        return self.x[: self.training_dt_size], self.y[: self.training_dt_size]

    def validation_sample(self):
        return self.x[self.training_dt_size :], self.y[self.training_dt_size :]    

    #returns a list of samples formed by sliding window
    #takes set as list and splits it to samples of k elements
    def sliding_window_samples(self, set, k):
        samples = []
        for i in range(len(set) - k):
            temp = []
            for j in range(k):
                temp.append(set[i + j])
            samples.append(temp)

        return samples            

    def sliding_window_e(self, set, k):
        return set[k :]

    def update_samples(self, k):
        training_set_x, training_set_e = self.training_sample()
        x_samples = self.sliding_window_samples(training_set_x, k)
        e_samples = self.sliding_window_e(training_set_e, k)

        data = x_samples
        for i in range(len(data)):
            data[i].append(e_samples[i])

        shuffled_data = np.asarray(data)
        np.random.shuffle(shuffled_data)

        e = shuffled_data[:, k:]
        e =  e.flatten() 

        return list(shuffled_data[:, :k]), e  
            



