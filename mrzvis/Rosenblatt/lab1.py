from numpy import random
from tabulate import tabulate

e = [1, 1, 1, 0]
x = [ [1, 1], [0, 1], [0, 0], [1, 0] ]
sample_size = len(x)
image_size  = len(x[0])

y = [0, 0, 0, 0]
w = [[random.random(), random.random()] for _ in range(sample_size)]
T = [random.random() for _ in range(sample_size)] 
S = [0, 0, 0, 0]
alpha = 0.5
EPOCH = 0

def weights_change_rule():
    for i in range(sample_size):
        for j in range(image_size):
            w[i][j] -= alpha * x[i][j] * (y[i] - e[i])

def threshold_change_rule():
    for i in range(sample_size):
        T[i] += alpha * (y[i] - e[i])

def weighted_sum():
    for i in range(sample_size):
        for j in range(image_size):
            S[i] += x[i][j]
        S[i] -= T[i]
            
def count_network_reaction():
    for i in range(sample_size):
        if S[i] >= 0:
            y[i] = 1
        else:
            y[i] = 0     

def print_parameters():
    headers = ['weights', 'T', '(x1, x2)', 'y', 'e']
    table   = zip(w, T, x, y, e)
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


while(True):
    weighted_sum()
    count_network_reaction()

    print_parameters()

    if y == e:
        break

    weights_change_rule()
    threshold_change_rule()
    EPOCH += 1
    
