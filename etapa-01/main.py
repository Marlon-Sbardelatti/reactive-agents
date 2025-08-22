from typing import Tuple
from simple_agent import SimpleAgent
import time


def main():
    grid_size = int(input("Defina n para o grid n x n: "))

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    agent = SimpleAgent(grid_size)

    while agent.position != (-1, -1):
        print(agent.position)
        print(agent.collided_walls)
        agent.move()
        time.sleep(1)

        grid = get_updated_grid(agent.position, grid_size)
        print_grid(grid)

    print("Objetivo concluído!!! :)")


def get_updated_grid(position: Tuple, grid_size: int):
    return [
        [
            1 if clmn == position[0] and row == position[1] else 0
            for clmn in range(grid_size)
        ]
        for row in range(grid_size)
    ]


def print_grid(grid):
    for row in grid:
        for element in row:
            print(f"{element:4}", end="")
        print()

    print("-----------------------------------------------------------", end="\n\n")


if __name__ == "__main__":
    main()
