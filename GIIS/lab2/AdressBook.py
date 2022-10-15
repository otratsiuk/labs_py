import json
import csv


class AdressBook:
    def __init__(self):
        self.book = {}


    def export(self, filename):
        headers = ["name", "adress"]
        with open(filename, 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow(headers)

            for k in self.book.keys():
                writer.writerow([k, self.book[k]])



    def save_to_file(self):
        with open('file.txt', 'w') as file:
            json.dump(self.book, file)


    def load_from_file(self):
        with open('file.txt', 'r') as f:
            data = f.read()
            self.book = json.loads(data)
            print(self.book)


    def prev_and_next(self, name):
        keys = list(sorted(self.book))
        i = None
        next = None
        prev = None
        if name in keys:
            i = keys.index(name)
            if i == 0:
                prev = keys[len(keys) - 1]
                next = keys[i + 1]

            elif i == len(keys) - 1:
                next = keys[0]
                prev = keys[i - 1]

            else:
                prev = keys[i - 1]
                next = keys[i + 1]

            return [prev, next]    

        return None        


    def remove_person(self, name):
        self.book.pop(name)


    def add_person(self, name, adress):
        self.book[name] = adress


    def get(self, name):
        if name in self.book:
            return [name, self.book[name]]

        return None    


    def size(self):
        return len(self.book)   
