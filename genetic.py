import time
from board import Board
import random
from math import comb


def mutate(genes, chance):
    r = random.random()
    if r <= chance:
        chosen_gene = random.randint(0, len(genes) - 1)
        index = random.randint(0, len(genes[0]) - 1)
        replacement_number = random.randint(0, len(genes[0]) - 1)

        old_gene = list(genes[chosen_gene])
        old_gene[index] = str(replacement_number)
        mutated_gene = ''.join(old_gene)
        genes[chosen_gene] = mutated_gene

    return genes


def crossover(genes, selections):
    # Check if we have an even number of genes
    if len(genes) % 2 == 1:
        return

    new_genes = []
    ranges = []
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

    if len(new_genes) != len(genes):
        print("Something fucked up")
        print(genes)
        print(new_genes)
        print(ranges)

    # Pair off your new genes
    pre_cross_pairs = {new_genes[i]: new_genes[i + 1] for i in range(0, len(new_genes), 2)}

    for p in pre_cross_pairs:
        split = random.randint(0, len(p) - 1)
        temp1 = p
        temp2 = pre_cross_pairs[p]

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
    return [x / fitness_sum for x in fitness]


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


def genetic_algorithm(states):

    genes = []  # Place holder for our genes

    # Randomly generate our genes to be used
    for i in range(states):
        gene_lst = []
        for j in range(states):
            gene_lst.append(random.randint(0, states - 1))

        gene = ''.join(str(n) for n in gene_lst)
        genes.append(gene)

    # Loop through the algorithm until the solution is found
    start = time.time()
    while not check(genes):
        sel = selection(genes)
        genes = crossover(genes, sel)
        genes = mutate(genes, 0.75)
    end = time.time()

    solution = str_to_board(check(genes))
    solution.gene_fitness()
    solution.show()
    running = int((end - start) * 1000)
    print("Running Time: " + f"{running:,}" + " ms")


if __name__ == '__main__':
    genetic_algorithm(8)
