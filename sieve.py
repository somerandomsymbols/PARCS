# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from os import stat
from Pyro4 import expose
from array import *


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        
    def solve(self):
        numbers = self.read_input()
        step = int(numbers[0]) / len(self.workers)
        mapped = []
        
        for i in range(0, len(self.workers) - 1):
            mapped.append(self.workers[i].mymap(i * step, (i + 1) * step))
        mapped.append(self.workers[len(self.workers) - 1].mymap((len(self.workers) - 1) * step, int(numbers[0])))
        
        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(a, b):
        res = []
        
        for k in range(a, b):
            i = k + 1
            if i == 1:
                continue
            elif i == 2:
                res.append(2)
            elif i % 2 != 0:
                n = 3
                
                while n * n <= i:
                    if i % n == 0:
                        break
                    n += 2

                if n * n > i:
                    res.append(i)
        
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        res = []
        for chunk in mapped:
            for s in chunk.value:
                res.append(s)
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        return [line.strip() for line in f.readlines()]

    def write_output(self, output):
        f = open(self.output_file_name, 'w')

        for s in output:
            f.write(str(s) + '\n')

        f.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
