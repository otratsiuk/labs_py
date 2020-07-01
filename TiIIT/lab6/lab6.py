import numpy as np
from math import sin

x = np.genfromtxt("x.csv")
y = np.genfromtxt("y.csv")

prev_w = []
curr_w = []
best_w = []

real_y_list = []

MAX_ITERS = 700
ITERS = 0

iteration = 0
W0 = np.random.uniform(0.0, 1)

for i in range(3):
    curr_w.append(np.random.uniform(0.0, 1))

best_w = curr_w


def count_y(curr_w):
    real_y = 0
    for i in range(3):
        real_y += curr_w[i] * x[iteration][i]
    return real_y + W0


def MSE(real_y_list):
    mse = np.mean(y - real_y_list)
    return abs(mse)


def cout_y_for_sin(curr_w):
    S = 0
    for i in range(3):
        S += curr_w[i] * x[iteration][i]
    real_y = sin(S + W0)
    return real_y


# first generation for linear model
while (iteration < 200):
    real_y = count_y(curr_w)
    real_y_list.append(real_y)
    iteration += 1
mse = MSE(real_y_list)
best_w = curr_w
best_mse = mse

# search for the best generation for linear model
while(ITERS < MAX_ITERS):
    real_y_list.clear()
    iteration = 0
    prev_w = curr_w
    curr_w.clear()
    for i in range(3):
        curr_w.append(np.random.uniform(0.0, 1))

    while (iteration < 200):
        real_y = count_y(curr_w)
        real_y_list.append(real_y)
        iteration += 1
    mse = MSE(real_y_list)
    if(mse < best_mse):
        best_w = curr_w
        best_mse = mse
    ITERS += 1

print(str('\nbest MSE for linear regression: ') + str(best_mse))
print(str('best parameters for linear model:\n ') + str(best_w))


# first generation for trigonometric model
curr_w2 = []
for i in range(3):
    curr_w2.append(np.random.uniform(0.0, 1))
real_y_list2 = []
iteration = 0
while (iteration < 200):
    real_y2 = cout_y_for_sin(curr_w2)
    real_y_list2.append(real_y2)
    iteration += 1
mse2 = MSE(real_y_list2)
best_w2 = curr_w2
best_mse2 = mse2

# search for the best generation for trigonometric model
ITERS = 0
while(ITERS < MAX_ITERS):
    real_y_list.clear()
    iteration = 0
    prev_w2 = curr_w2
    curr_w2.clear()
    for i in range(3):
        curr_w2.append(np.random.uniform(0.0, 1))

    while (iteration < 200):
        real_y2 = cout_y_for_sin(curr_w2)
        real_y_list.append(real_y2)
        iteration += 1
    mse2 = MSE(real_y_list2)
    if(mse < best_mse):
        best_w2 = curr_w2
        best_mse2 = mse2
    ITERS += 1

print(str('\nbest MSE for trigonometric regression: ') + str(best_mse2))
print(str('best parameters for non-linear model:\n ') + str(best_w2)+str('\n'))
