import numpy as np
import math
import random
from PIL import Image


class MedianFilter():
    def __init__(self):
        self.filename = ''
        self.arr = np.array
        self.noised_arr = np.array
        self.edited_arr = np.array
        self.edited_image_filename = ''


    def open_image(self, filename):
        self.filename = filename
        self.img = Image.open(self.filename).convert("L")
        self.arr = np.array(self.img)
        self.edited_arr = np.copy(self.arr)
        self.noised_arr = np.copy(self.arr)


    def add_zero_padding(self, n):
        self.edited_arr = np.pad(self.noised_arr, n, 'constant')


    def size(self):
        row, col = self.edited_arr.shape
        return (row, col)    


    def add_noise(self, n):
        number_of_pixels = random.randint(0, n)
        self.noised_arr = np.copy(self.arr)
        row, col = self.noised_arr.shape

        for i in range(number_of_pixels):
            y_coord = random.randint(0, row - 1)
            x_coord = random.randint(0, col - 1)
            
            self.noised_arr[y_coord][x_coord] = 255
            
        number_of_pixels = random.randint(0, n)
        for i in range(number_of_pixels):
            y_coord=random.randint(0, row - 1)
            x_coord=random.randint(0, col - 1)
            
            self.noised_arr[y_coord][x_coord] = 0

        self.save_noised_image("noised_temp")
        self.edited_arr = np.copy(self.noised_arr)    


    def apply(self, window_size):
        self.edited_arr = np.copy(self.noised_arr) 
        result = []
        width = self.edited_arr.shape[0]
        height = self.edited_arr.shape[1]
        median = math.floor(window_size**2 / 2)
        self.add_zero_padding(math.floor(window_size / 2))
        print(self.edited_arr)
        print(len(self.edited_arr))
        

        i = 0
        while i < len(self.edited_arr) - (window_size - 1):
            j = 0
            mask = []

            while j < len(self.edited_arr[i]):
                for x in range(i, i + window_size):
                    mask.append(self.edited_arr[x][j])

                if len(mask) == window_size**2:
                    mask.sort()
                    result.append(mask[median])

                    j -= (window_size - 1)
                    mask.clear()

                j += 1    

            i += 1    
            
        self.edited_arr = np.reshape(np.asarray(result), (width, height))
        self.save_edited_image('edited_temp')
        self.edited_arr = np.copy(self.arr)


    def save_edited_image(self, filename):
        self.edited_image = Image.fromarray(self.edited_arr).convert('RGB')
        self.edited_image.save(filename, format='png')

    def save_noised_image(self, filename):
        self.noised_image = Image.fromarray(self.noised_arr).convert('RGB')
        self.noised_image.save(filename, format='png')
