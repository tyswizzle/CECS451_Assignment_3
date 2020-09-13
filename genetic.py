from board import Board
import random
from math import comb


def mutate(genes, chance):
    r = random.random()
    if r <= chance:
        chosen_gene = random.randint(0, len(genes) - 1)
        index = random.randint(0, len(genes[0]) - 1)
        replacement_number = random.randint(0, len(genes[0]) - 1)

        old_gene = genes[chosen_gene]
        genes[chosen_gene] = old_gene[:index - 1] + str(replacement_number) + old_gene[index:]

    return genes


def crossover(genes, selections):
    # Check if we have an even number of genes
    if len(genes) % 2 == 1:
        return
    num_pairs = len(genes) / 2
    new_genes = []
    ranges = []
    pre_cross_pairs = {}
    post_cross_genes = []
    for i in range(len(selections)):
        if i == 0:
            ranges.append(selections[i])
        else:
            ranges.append(ranges[i - 1] + selections[i])

    # Select your new genes based on the given selection percentages
    for i in range(len(genes)):
        r = random.random()
        for j, y in enumerate(ranges):
            if y > r:
                new_genes.append(genes[i - 1])
                break

    # Pair off your new genes
    n = 0
    while n <= num_pairs:
        pre_cross_pairs[(new_genes[n], new_genes[n + 1])] = random.randint(0, len(genes[0]) - 1)
        n += 2

    for p in pre_cross_pairs:
        split = int(pre_cross_pairs[p])
        temp1 = p[0]
        temp2 = p[1]

        post_cross_genes.append(temp1[:split] + temp2[split:])
        post_cross_genes.append(temp2[:split] + temp1[split:])

    return post_cross_genes


def selection(genes):
    boards = []
    fitness = []
    for gene in genes:
        board = str_to_board(gene)
        board.gene_fitness()
        boards.append(board)
        fitness.append(board.get_fit())
    fitness_sum = sum(fitness)
    return [round(x / fitness_sum,2) for x in fitness]


def str_to_board(gene_string):

    gene = list(map(int, gene_string))
    board = Board(len(gene))
    for row in range(board.n_queen):
        current_pos = [idx for idx, val in enumerate(board.get_map()[row]) if val != 0][0]
        if current_pos != gene[row] - 1:
            board.flip(row, current_pos)
            board.flip(row, gene[row] - 1)
    return board


def check(genes):
    goal = comb(len(genes[0]), 2)

    for gene in genes:
        gene_board = str_to_board(gene)
        gene_board.gene_fitness()
        if gene_board.get_fit() == goal:
            return gene

    return None

if __name__ == '__main__':

    # size = 8
    # gene_string = "32543213"
    # test = str_to_board(gene_string)
    # test.gene_fitness()
    # test.show()
    genes = ['24748552', '32752411', '24415124', '32543213']
    while not check(genes):
        sel = selection(genes)
        genes = crossover(genes, sel)
        genes = mutate(genes, 1)

    solution = str_to_board(check(genes))
    solution.gene_fitness()
    solution.show()
