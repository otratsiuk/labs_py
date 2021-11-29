import math
import matplotlib.pyplot as plt
from scipy.special import expit
import numpy as np
import random
from Dataset import Dataset

class MLP:
    alpha = 0.01
    Emin  = 1
    dataset_size = 2000

    def __init__(self, input_layer_size, hidden_layer_size):
        self.input_layer_size  = input_layer_size
        self.hidden_layer_size = hidden_layer_size

        self.y = np.asarray([0.0 for _ in range(hidden_layer_size)])

        self.wi  = np.asarray([[random.uniform(0, 0.5) for _ in range(input_layer_size)] for _ in range(hidden_layer_size)])
        self.wj = np.asarray([random.uniform(0, 0.5) for _ in range(hidden_layer_size)])

        self.Ti  = np.asarray([random.uniform(0, 0.5) for _ in range(hidden_layer_size)]) 
        self.Tj = np.asarray(random.uniform(0, 0.5))

        self.window = []

    def func(self, x):
        return 0.4 * math.cos(0.2 * x) + 0.07 * math.sin(0.2 * x)

    def sigmoid_func(self, x, deriv=False):
        if (deriv == True):
            return x * (1 - x)
        return 1/(1 + np.exp(-x))      

    def calculate_hidden_layer_activity(self, x):
        self.y = expit(np.subtract(np.dot(x, self.wi.T), self.Ti))

    def calculate_output_layer_activity(self):
        return np.subtract(np.dot(self.y, self.wj), self.Tj)

    def feedforward(self, X):
        self.calculate_hidden_layer_activity(X)
        return self.calculate_output_layer_activity()        

    def backward(self, X, e, output):
        self.output_error = e - output

        self.hidden_error = np.dot(self.wj, self.output_error)

        self.wj -= self.alpha * np.dot(self.y, self.output_error)
        self.Tj += self.alpha * self.output_error

        self.wi -=  self.alpha * np.outer(np.dot(self.hidden_error, np.dot(self.y, np.subtract(1, self.y))), X) 
        self.Ti += self.alpha * (self.hidden_error * np.dot(self.y, np.subtract(1, self.y)))

        return self.output_error

    def learning(self):
        epoch = 1
        dataset = Dataset(self.dataset_size, self.func)
        training_set_x, training_set_e = dataset.training_sample()
        window_samples_x = dataset.sliding_window_samples(training_set_x, self.input_layer_size)
        window_sample_e = dataset.sliding_window_e(training_set_e, self.input_layer_size)
        
        E = self.Emin
        plt.ion()
        fig = plt.figure()
        while(E >= self.Emin):
            epoch += 1
            y_set = []
            E = 0
            for i in range(len(window_samples_x) - (self.input_layer_size + 1)):
                self.window = np.asarray(window_samples_x[i])
                
                y = self.feedforward(self.window)
                y_set.append(y)

                output_layer_mistake = self.backward(self.window, window_sample_e[i], y)
                E += pow(output_layer_mistake, 2)
                
            E *= 0.5
            print("E: " + str(E))    
            plt.plot(training_set_x[: len(y_set)], y_set)
            plt.plot(training_set_x[: len(window_sample_e)], window_sample_e, "yellow")
            plt.draw()
            plt.pause(0.1) 
            fig.clear() 

    def prognosticate(self):
        y = []

        dataset = Dataset(self.dataset_size, self.func)
        validation_set_x, validation_set_e = dataset.validation_sample()
        window_samples_x = dataset.sliding_window_samples(validation_set_x, self.input_layer_size)

        for w in window_samples_x:
            self.window = np.asarray(w)
            self.feedforward(self.window)

        plt.plot(validation_set_x[: len(y)], y, "red")
        #plt.plot(validation_set_x, validation_set_e, "red")
        plt.show()
        plt.pause(0.1)


x = MLP(8, 3)
x.learning()
x.prognosticate()