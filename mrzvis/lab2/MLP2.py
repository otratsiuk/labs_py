import math
import matplotlib.pyplot as plt
from scipy.special import expit
import numpy as np
import random
from Dataset import Dataset

class MLP:
    alpha = 0.3
    Emin  = 0.0001
    dataset_size = 1000

    def __init__(self, input_layer_size, hidden_layer_size):
        self.input_layer_size  = input_layer_size
        self.hidden_layer_size = hidden_layer_size


        self.y = np.asarray([0.0 for _ in range(hidden_layer_size)])
        
        self.wi  = np.asarray([[random.uniform(0, 0.9) for _ in range(input_layer_size)] for _ in range(hidden_layer_size)])
        
        self.wj = np.asarray([random.uniform(0, 0.9) for _ in range(hidden_layer_size)])

        self.Ti  = np.asarray([random.uniform(0, 0.9) for _ in range(hidden_layer_size)]) 
        self.Tj = np.asarray(random.uniform(0, 0.9))

        self.window = []

    def func(self, x):
        return 0.4 * math.cos(0.2 * x) + 0.07 * math.sin(0.2 * x)

    def sigmoid_func(self, x, deriv=False):
        if (deriv == True):
            return x * (1 - x)
        return 1/(1 + np.exp(-x))      


    def calculate_hidden_layer_activity(self, x):
        self.y = expit(np.subtract(np.dot(self.wi, x), self.Ti))

    def calculate_output_layer_activity(self):
        return np.dot(self.wj, self.y) - self.Tj

    def feedforward(self, X):
        self.calculate_hidden_layer_activity(X)
        return self.calculate_output_layer_activity()        

    def backward(self, X, e, output):
        self.output_error = e - output

        self.hidden_error = self.wj * self.output_error
    
        self.wj = np.add(self.wj, self.alpha * self.output_error * self.y)
        self.Tj -= self .alpha * self.output_error

        gradient_i = self.hidden_error * (self.y * np.subtract(1, self.y))
        self.wi = np.add(self.wi, self.alpha * np.outer(gradient_i, X))
        self.Ti = np.subtract(self.Ti, self.alpha * gradient_i)
        return self.output_error

    def learning(self):
        dataset = Dataset(self.dataset_size, self.func)
        E = self.Emin
        
        window_samples_x, window_sample_e = dataset.update_samples(self.input_layer_size)

        while(E >= self.Emin):
            #window_samples_x, window_sample_e = dataset.update_samples(self.input_layer_size)

            y_set = []
            E = 0
            for i in range(len(window_samples_x)):
                self.window = np.asarray(window_samples_x[i])
                
                y = self.feedforward(self.window)
                y_set.append(y)

                output_layer_mistake = self.backward(self.window, window_sample_e[i], y)
                E += pow(output_layer_mistake, 2)
                
            E *= 0.5
            print("E: " + str(E))    

    def prognosticate(self):
        y = []

        dataset = Dataset(self.dataset_size, self.func)
        validation_set_x, validation_set_e = dataset.validation_sample()

        window_samples_x = dataset.sliding_window_samples(validation_set_x, self.input_layer_size)
        window_sample_e = dataset.sliding_window_e(validation_set_e, self.input_layer_size)

        for w in window_samples_x:
            self.window = np.asarray(w)
            y.append(self.feedforward(self.window))

        plt.plot(validation_set_x[: len(y)], y, "red")
        plt.plot(validation_set_x[: len(window_sample_e)], window_sample_e, "green")
        plt.show()


x = MLP(8, 3)
x.learning()
x.prognosticate()