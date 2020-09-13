import random
from math import comb
import numpy as np


class Board:
    def __init__(self, n):
        self.n_queen = n
        self.map = [[0 for j in range(n)] for i in range(n)]
        self.fit = 0

        for i in range(self.n_queen):
            j = random.randint(0, self.n_queen - 1)
            self.map[i][j] = 1

    def fitness(self):
        self.fit = 0
        for i in range(self.n_queen):
            for j in range(self.n_queen):
                if self.map[i][j] == 1:
                    for k in range(1, self.n_queen - i):
                        if self.map[i + k][j] == 1:
                            self.fit += 1
                        if j - k >= 0 and self.map[i + k][j - k] == 1:
                            self.fit += 1
                        if j + k < self.n_queen and self.map[i + k][j + k] == 1:
                            self.fit += 1

    def gene_fitness(self):
        self.fit = comb(self.n_queen, 2)
        for i in range(self.n_queen):
            for j in range(self.n_queen):
                if self.map[i][j] == 1:
                    for k in range(1, self.n_queen - i):
                        if self.map[i + k][j] == 1:
                            self.fit -= 1
                        if j - k >= 0 and self.map[i + k][j - k] == 1:
                            self.fit -= 1
                        if j + k < self.n_queen and self.map[i + k][j + k] == 1:
                            self.fit -= 1

    def show(self):
        print(np.matrix(self.map))
        print("Fitness: ", self.fit)

    def flip(self, i, j):
        if self.map[i][j] == 0:
            self.map[i][j] = 1
        else:
            self.map[i][j] = 0

    def get_map(self):
        return self.map

    def get_fit(self):
        return self.fit

    def __hash__(self):
        hashed = ""
        for row in range(self.n_queen):
            for col in range(self.n_queen):
                hashed += str(self.map[row][col])
        return hash(hashed)

    def __eq__(self, other):
        return np.array_equal(self.map, other.map)

    def __ne__(self, other):
        return not(self == other)


if __name__ == '__main__':
    size = 5
    test = Board(size)
    test.fitness()
    test.show()