from utility_based_agent import UtilityBasedAgent
from typing import List, Tuple
from random import randint, shuffle
import time
from termcolor import colored


def main():
    is_default = int(
        input("Opções de mapa de obstáculos\n1 - Padrão\n2 - Aleatório\nEscolha: ")
    )

    if is_default == 1:
        grid_size = 10
        grid_weights = generate_default_cell_weights()
        initial_position = (0, 5)
        target = (9, 5)

    else:
        grid_size = int(input("Escolha o tamanho do tabuleiro: "))
        grid_weights = generate_random_cell_weights(grid_size)
        initial_position = generate_random_position(grid_size)
        target = generate_random_position(grid_size)

        while target == initial_position:
            target = generate_random_position(grid_size)

        grid_weights[initial_position[0]][initial_position[1]] = 0
        grid_weights[target[0]][target[1]] = 0

    grid = [[_ for _ in range(grid_size)] for _ in range(grid_size)]

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


def generate_default_cell_weights():
    return [
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 3, 1, 1, 1, 1],
        [1, 1, 2, 2, 1, 3, 3, 2, 1, 1],
        [1, 1, 2, 1, 3, 3, 3, 2, 1, 1],
        [1, 1, 2, 2, 3, 3, 3, 2, 2, 1],
        [1, 1, 1, 2, 3, 1, 2, 2, 1, 1],
        [1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    ]


def get_weight_color(cell: int) -> str:
    match cell:
        case 1:
            return "green"
        case 2:
            return "yellow"
        case 3:
            return "red"
        case _:
            return "white"


def generate_random_cell_weights(grid_size):
    # Células normais (1)
    weights = [[1 for _ in range(grid_size)] for _ in range(grid_size)]

    total_cells = grid_size * grid_size
    sandy_cells_count = randint(1, total_cells // 2)
    rocky_cells_count = randint(1, total_cells // 2)

    all_positions = [
        (row, clmn) for row in range(grid_size) for clmn in range(grid_size)
    ]
    shuffle(all_positions)

    # Células arenosas (2)
    for row, clmn in all_positions[:sandy_cells_count]:
        weights[row][clmn] = 2

    # Células rochosas (3)
    for row, clmn in all_positions[
        sandy_cells_count : sandy_cells_count + rocky_cells_count
    ]:
        weights[row][clmn] = 3

    return weights


def generate_random_position(grid_size) -> Tuple:
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
        weight = grid_weights[row][clmn]
        return colored(weight, get_weight_color(weight))


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
