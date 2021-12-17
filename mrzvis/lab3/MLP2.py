from scipy.special import expit
import numpy as np
import random
from Dataset import Dataset
from tabulate import tabulate

class MLP:
    alpha = 0.01
    Emin  = 0.0001

    def __init__(self, input_layer_size, hidden_layer_size, output_layer_size):
        self.input_layer_size  = input_layer_size
        self.hidden_layer_size = hidden_layer_size

        self.y  = np.asarray([0.0 for _ in range(hidden_layer_size)])
        
        self.wi = np.asarray([[random.uniform(-0.5, 0.5) for _ in range(input_layer_size)] for _ in range(hidden_layer_size)])
        self.wj = np.asarray([[random.uniform(-0.5, 0.5) for _ in range(hidden_layer_size)] for _ in range(output_layer_size)])

        self.Ti = np.asarray([random.uniform(-0.5, 0.5) for _ in range(hidden_layer_size)]) 
        self.Tj = np.asarray([random.uniform(-0.5, 0.5) for _ in range(output_layer_size)])

        self.output = np.asarray([0.0 for _ in range(output_layer_size)])

    def feedforward(self, X):
        self.y = expit(np.subtract(np.dot(self.wi, X), self.Ti))

        return np.dot(self.wj, self.y) - self.Tj

    def backward(self, X, e):
        self.output_error = self.output - e

        self.hidden_error = np.dot(self.output_error, self.wj)
    
        self.wj -= self.alpha * np.outer(self.output_error, self.y)
        self.Tj += self.alpha * self.output_error

        gradient_i = self.hidden_error * (self.y * (1 - self.y))
        self.wi    -= self.alpha * np.outer(gradient_i, X)
        self.Ti    += self.alpha * gradient_i

    def cost_function(self, inputs, e):
        err = 0
        for i in range(len(inputs)):
            err += (e[i] - self.feedforward(inputs[i])) ** 2

        return err * 0.5    

    def learning(self, inputs, e):
        E = self.Emin

        while(np.sum(E) >= self.Emin):
            y_set = []
            E = 0
            for i in range(len(inputs)):
                X = np.asarray(inputs[i])
                
                self.output = self.feedforward(X)
                y_set.append(self.output)

                self.backward(X, e[i])

                E = self.cost_function(inputs, e) 
                print('Err: ' + str(np.sum(E)))

                if np.sum(E) < self.Emin:
                    break  

    def forecast(self, inputs):
        y_set = []
        for i in range(len(inputs)):
            X = np.asarray(inputs[i])
            y = self.feedforward(X)

            y_set.append(y)

        return y_set 

    def print_results(self, e, y, num_of_changed_bits, letters):
        headers = ['recognized image', letters, 'number of changed bits']
        table   = zip(y, e, num_of_changed_bits)   
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

dataset = Dataset()
inputs_t, e_t = dataset.get_training_sample()
inputs_v, e_v = dataset.get_validation_sample()

mlp = MLP(30, 15, 3)
mlp.learning(inputs_t, e_t)
y = mlp.forecast(inputs_v)

mlp.print_results(e_v, y, dataset.number_of_changed_bits, dataset.letters)
