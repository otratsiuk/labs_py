import math

precision = 0.0001
step = 0.001
MAX_ITERS = 1000

X = float(input('Enter start point x: '))
Y = float(input('Enter start point y: '))
Z = float(input('Enter start point z: '))

left_border = -50
right_border = 50


def function(x, y, z): return round(math.pow(y, 2) + (1+y*math.pow(z, 2)) *
                                    math.sin(x) + 2*math.pow(y, 4)*(x + 2), 4)


def df_dx(x, y, z): return round(math.pow(y, 2) +
                                 (1 + y*math.pow(z, 2)) * math.cos(x) + 6*math.pow(y, 4), 4)


def df_dy(x, y, z): return round(2*y + (1 + math.pow(z, 2)) *
                                 math.sin(x) + 8*math.pow(y, 3)*(x+2), 4)


def df_dz(x, y, z): return round(math.pow(y, 2) + (1+2*y*z) *
                                 math.sin(x) + 2*math.pow(y, 4)*(x+2), 4)


def delta(current, previous):
    return bool(math.fabs(current - previous) > precision)


def max():
    previous_x = X
    previous_y = Y
    previous_z = Z

    current_x = X + step * df_dx(X, Y, Z)
    current_y = Y + step * df_dy(X, Y, Z)
    current_z = Z + step * df_dz(X, Y, Z)

    print(function(current_x, current_y, current_z),
          current_x, current_y, current_z)

    iters_counter = 1
    process = 1

    while iters_counter < MAX_ITERS and process:
        if delta(current_x, previous_x):
            current_x = round(current_x + step * df_dx(previous_x, Y, Z), 4)
            previous_x = current_x
        if delta(current_y, previous_y):
            previous_y = current_y
            current_y = round(current_y + step * df_dy(X, previous_y, Z), 4)
        if delta(current_z, previous_z):
            previous_z = current_z
            current_z = round(current_z + step * df_dz(X, Y, previous_z), 4)

        if function(current_x, current_y, current_z) > left_border and function(current_x, current_y, current_z) < right_border:
            print(function(current_x, current_y, current_z),
                  current_x, current_y, current_z)
        else:
            process = 0

        iters_counter += 1


def min():
    previous_x = X
    previous_y = Y
    previous_z = Z

    current_x = X - step * df_dx(X, Y, Z)
    current_y = Y - step * df_dy(X, Y, Z)
    current_z = Z - step * df_dz(X, Y, Z)

    print(function(current_x, current_y, current_z),
          current_x, current_y, current_z)

    iters_counter = 1
    process = 1

    while iters_counter < MAX_ITERS and process:
        if delta(current_x, previous_x):
            current_x = round(current_x - step * df_dx(previous_x, Y, Z), 4)
            previous_x = current_x
        if delta(current_y, previous_y):
            previous_y = current_y
            current_y = round(current_y - step * df_dy(X, previous_y, Z), 4)
        if delta(current_z, previous_z):
            previous_z = current_z
            current_z = round(current_z - step * df_dz(X, Y, previous_z), 4)

        if function(current_x, current_y, current_z) > left_border and function(current_x, current_y, current_z) < right_border:
            print(function(current_x, current_y, current_z),
                  current_x, current_y, current_z)
        else:
            process = 0

        iters_counter += 1


vector = input('Enter min or max: ')

if vector == 'min':
    min()
elif vector == 'max':
    max()
