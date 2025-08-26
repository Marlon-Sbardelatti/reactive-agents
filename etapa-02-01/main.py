from random import randint
from typing import Tuple
from simple_agent import SimpleAgent
import time


def main():
    grid_size = int(input("Escolha o tamanho do tabuleiro: "))

    grid = [[_ for _ in range(grid_size)] for _ in range(grid_size)]

    initial_position = create_random_position(grid_size)
    agent = SimpleAgent(grid_size, initial_position)

    while not agent.has_finished():
        agent.move()
        time.sleep(1)

        grid = get_updated_grid(agent, grid_size)
        print_grid(grid)
    print(agent.get_results())


def create_random_position(grid_size) -> Tuple:
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return (x, y)


def get_updated_grid(agent: SimpleAgent, grid_size: int):
    return [
        [get_cell_value(row, clmn, agent) for clmn in range(grid_size)]
        for row in range(grid_size)
    ]

def get_cell_value(row: int, clmn: int, agent: SimpleAgent) -> str:
    def same_position(cell: Tuple, position: Tuple):
        return cell == position

    current_cell = (row, clmn)

    if same_position(current_cell, agent.position):
        return "♟"  # Player
    elif current_cell in agent.memory and not same_position(
        current_cell, agent.position
    ):
        return "▪"  # Caminho
    else:
        return " "  # Espaço vazio


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
