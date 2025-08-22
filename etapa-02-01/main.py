from typing import Tuple
from simple_agent import SimpleAgent
import time


def main():
    grid_size = int(input("Defina n para o grid n x n: "))

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    agent = SimpleAgent(grid_size)

    while agent.position != (-1, -1):
        print(agent.position)
        agent.move()
        time.sleep(1)

        grid = get_updated_grid(agent, grid_size)
        trace(agent, grid)
        print_grid(grid)

    print("Objetivo concluído!!! :)")


def get_updated_grid(agent: SimpleAgent, grid_size: int):
    return [
        [define_type(clmn, row, agent) for clmn in range(grid_size)]
        for row in range(grid_size)
    ]


def trace(agent: SimpleAgent, grid):
    for m in agent.memory:
        # print("agent position: ", agent.position, "m: ", m)
        if agent.position != m:
            grid[m[1]][m[0]] = 3


def define_type(clmn: int, row: int, agent: SimpleAgent) -> int:
    if clmn == agent.position[0] and row == agent.position[1]:
        return 1
    else:
        return 0


def print_grid(grid):
    for row in grid:
        for element in row:
            print(f"{element:4}", end="")
        print()

    print("-----------------------------------------------------------", end="\n\n")


if __name__ == "__main__":
    main()
