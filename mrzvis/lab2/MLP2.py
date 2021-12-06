import math
import matplotlib.pyplot as plt
from scipy.special import expit
import numpy as np
import random
from Dataset import Dataset

class MLP:
    alpha = 0.001
    Emin  = 0.1
    dataset_size = 4000

    def __init__(self, input_layer_size, hidden_layer_size):
        self.input_layer_size  = input_layer_size
        self.hidden_layer_size = hidden_layer_size

        self.y  = np.asarray([0.0 for _ in range(hidden_layer_size)])
        
        self.wi = np.asarray([[random.uniform(-0.5, 0.5) for _ in range(input_layer_size)] for _ in range(hidden_layer_size)])
        self.wj = np.asarray([random.uniform(-0.5, 0.5) for _ in range(hidden_layer_size)])

        self.Ti = np.asarray([random.uniform(-0.5, 0.5) for _ in range(hidden_layer_size)]) 
        self.Tj = np.asarray(random.uniform(-0.5, 0.5))

        self.output = 0

    def func(self, x):
        return 0.4 * math.cos(0.2 * x) + 0.07 * math.sin(0.2 * x)  

    def feedforward(self, X):
        self.y = expit(np.subtract(np.dot(self.wi, X), self.Ti))

        return np.dot(self.wj, self.y) - self.Tj

    def backward(self, X, e):
        self.output_error = self.output - e

        self.hidden_error = self.wj * self.output_error
    
        self.wj -= self.alpha * self.output_error * self.y
        self.Tj += self.alpha * self.output_error

        gradient_i = self.hidden_error * (self.y * (1 - self.y))
        self.wi    -= self.alpha * np.outer(gradient_i, X)
        self.Ti    += self.alpha * gradient_i

    def cost_function(self, x_windows, e):
        err = 0
        for i in range(len(x_windows)):
            err += (e[i] - self.feedforward(x_windows[i])) ** 2

        return err * 0.5    

    def plotter(self, t, y, e, title):
        plt.title(title)
        plt.plot(t[: len(y)], y, "red", label='forecast')
        plt.plot(t[: len(y)], e, "blue", label='original')
        plt.legend()
        plt.show()

    def learning(self):
        dataset = Dataset(self.dataset_size, self.func)
        E = self.Emin
        
        x_windows, e = dataset.sliding_window_samples(dataset.training_sample(), self.input_layer_size)

        while(E >= self.Emin):
            y_set = []
            E = 0
            for i in range(len(x_windows)):
                X = np.asarray(x_windows[i])
                
                self.output = self.feedforward(X)
                y_set.append(self.output)

                self.backward(X, e[i])

                E = self.cost_function(x_windows, e) 
                print(E)  

                if E < self.Emin:
                    break

        y = []
        t = dataset.training_time_points()
        for i in x_windows:
            X = np.asarray(i)
            y.append(self.feedforward(X))

        self.plotter(t, y, e, 'Training interval')

    def forecast(self):
        y = []

        dataset = Dataset(self.dataset_size, self.func)
        forecasting_set_x = dataset.forecasting_sample()

        x_windows, e = dataset.sliding_window_samples(forecasting_set_x, self.input_layer_size)
        t = dataset.forecasting_time_points()

        for i in x_windows:
            X = np.asarray(i)
            y.append(self.feedforward(X))

        self.plotter(t, y, e, 'Forecasting interval')

mlp = MLP(8, 3)
mlp.learning()
mlp.forecast()