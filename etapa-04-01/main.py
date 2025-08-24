from typing import List, Tuple
import time
from utility_based_agent import UtilityBasedAgent
import random
from random import randint


def main():
    grid_size = int(input("Escolha o tamanho do tabuleiro: "))

    grid = [[_ for _ in range(grid_size)] for _ in range(grid_size)]
    grid_weights = create_cell_weights(grid_size)

    initial_position = create_random_position(grid_size)
    target = create_random_position(grid_size)

    while target == initial_position:
        target = create_random_position(grid_size)

    grid_weights[initial_position[0]][initial_position[1]] = 0
    grid_weights[target[0]][target[1]] = 0

    agent = UtilityBasedAgent(grid_size, grid_weights, initial_position)
    agent.set_target(target)

    while not agent.has_finished():
        grid = get_updated_grid(agent, grid_size, grid_weights)
        print_grid(grid)

        agent.move()
        time.sleep(1)

    print(agent.get_results())


def get_updated_grid(agent: UtilityBasedAgent, grid_size: int, grid_weights: List):
    return [
        [get_cell_value(row, clmn, agent, grid_weights) for clmn in range(grid_size)]
        for row in range(grid_size)
    ]


def create_cell_weights(grid_size):
    # Células normais (1)
    weights = [[1 for _ in range(grid_size)] for _ in range(grid_size)]

    total_cells = grid_size * grid_size
    sandy_cells_count = random.randint(1, total_cells // 2)
    rocky_cells_count = random.randint(1, total_cells // 2)

    all_positions = [
        (row, clmn) for row in range(grid_size) for clmn in range(grid_size)
    ]
    random.shuffle(all_positions)

    # Células arenosas (2)
    for row, clmn in all_positions[:sandy_cells_count]:
        weights[row][clmn] = 2

    # Células rochosas (3)
    for row, clmn in all_positions[
        sandy_cells_count : sandy_cells_count + rocky_cells_count
    ]:
        weights[row][clmn] = 3

    return weights


def create_random_position(grid_size) -> Tuple:
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return (x, y)


def get_cell_value(
    row: int, clmn: int, agent: UtilityBasedAgent, grid_weights: List
) -> str:
    def same_position(cell: Tuple, position: Tuple):
        return cell == position

    current_cell = (row, clmn)

    if same_position(current_cell, agent.position):
        return "♟"  # Player
    elif same_position(current_cell, agent.target):
        return "X"  # Alvo
    elif current_cell in agent.memory and not same_position(
        current_cell, agent.position
    ):
        return "▪"  # Caminho
    else:
        return grid_weights[row][clmn]  # Espaço vazio


def print_grid(grid):
    rows = len(grid)
    cols = len(grid[0])

    print("   " + "   ".join(str(c) for c in range(cols)))
    print("  +" + "---+" * cols)

    for r in range(rows):
        row_str = f"{r} |"
        for c in range(cols):
            row_str += f" {grid[r][c]} |"
        print(row_str)

        print("  +" + "---+" * cols)

    print("")


if __name__ == "__main__":
    main()

