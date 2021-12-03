import numpy as np

class Dataset:
    dt_splitter = 2 / 3

    def __init__(self, dt_size, function):
        self.dt_size = dt_size
        self.func = function

        self.training_dt_size = round(self.dt_size * self.dt_splitter)
        self.validation_dt_size = self.dt_size - self.training_dt_size

        self.t = np.linspace(-30, 30, self.dt_size)
        self.y = []
        for t in self.t:
            self.y.append(self.func(t))    

    def training_sample(self):
        return self.y[: self.training_dt_size]

    def validation_sample(self):
        return self.y[self.training_dt_size :]

    def time_points(self):
        return self.t[self.training_dt_size :]      

    def sliding_window_samples(self, set, k):
        samples = []
        for i in range(len(set) - k):
            temp = []
            for j in range(k):
                temp.append(set[i + j])
            samples.append(temp)

        return samples, set[k :]            
        