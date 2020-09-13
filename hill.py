from board import Board
import time
import copy


def hill_climb(original_board):

    solution = copy.deepcopy(original_board)
    solution.fitness()
    fit = solution.get_fit()
    board_size = solution.n_queen

    # Set maximum attempts at 10 times completely through
    max_iterations = (board_size - 1) * 10
    count = 0

    while fit != 0:  # Check if the board is already in a solution state
        for row in range(board_size):  # For Each row
            neighbors = get_neighbors(solution, row)
            solution = get_best_neighbor(neighbors)
            fit = solution.get_fit()
        count += 1
        if count == max_iterations:
            return None

    return solution


def get_neighbors(board, row):
    neighbors = {}  # mapped as board:if checked
    current_pos = [idx for idx, val in enumerate(board.get_map()[row]) if val != 0][0]
    for possible in range(board.n_queen):
        if possible != current_pos:  # Only check states that will be different than ours
            test = copy.deepcopy(board)  # Create a copy of the board to use
            test.flip(row, current_pos)  # Prepare to move the queen by resetting the row to all 0s
            test.flip(row, possible)  # Place the queen in its new position
            test.fitness()  # Calculate the new heuristic
            neighbors[test] = False  # Add this iteration to the list of possible neighbors

    return neighbors


def get_best_neighbor(neighbors):
    best_fit = 99
    for neighbor in neighbors:
        # Check if the neighbor has a better fit and hasn't been iterated through
        if neighbor.get_fit() < best_fit and not(neighbors[neighbor]):
            best_fit = neighbor.get_fit()
            best_neighbor = neighbor
    neighbors[best_neighbor] = True
    return best_neighbor


if __name__ == '__main__':
    size = 5
    solution = None
    restarts = -1
    start = time.time()
    while not solution:
        restarts += 1
        board = Board(size)
        solution = hill_climb(board)
    end = time.time()
    running = int((end - start) * 1000)
    solution.show()
    print("Running Time: " + f"{running:,}" + " ms")
    print("# of Restarts: " + str(restarts))
