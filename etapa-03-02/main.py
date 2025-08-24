from random import randint
from typing import List, Tuple
import time
from goal_based_agent import GoalBasedAgent


def main():
    grid_size = int(input("Escolha o tamanho do tabuleiro: "))

    grid = [[_ for _ in range(grid_size)] for _ in range(grid_size)]

    obstacles = generate_obstacles(grid_size)

    agent = GoalBasedAgent(grid_size, obstacles)

    while not agent.has_finished():
        agent.move()
        time.sleep(1)

        grid = get_updated_grid(agent, grid_size)
        print_grid(grid)

    print(agent.get_results())


def get_updated_grid(agent: GoalBasedAgent, grid_size: int):
    return [
        [get_cell_value(clmn, row, agent) for clmn in range(grid_size)]
        for row in range(grid_size)
    ]


def generate_obstacles(grid_size: int) -> List[Tuple]:
    obstacles = []

    obstacles_length = randint(1, (pow(grid_size, 2) // 2))

    for _ in range(obstacles_length):
        x = randint(0, grid_size - 1)
        y = randint(0, grid_size - 1)
        obstacles.append((x, y))

    return obstacles


def get_cell_value(clmn: int, row: int, agent: GoalBasedAgent) -> str:
    def same_position(cell: Tuple, position: Tuple):
        return cell == position

    current_cell = (clmn, row)

    if same_position(current_cell, agent.position):
        return "♟"  # Player
    elif same_position(current_cell, agent.target):
        return "X"  # Alvo
    elif current_cell in agent.memory and not same_position(
        current_cell, agent.position
    ):
        return "▪"  # Caminho
    elif current_cell in agent.obstacles:
        return "■"  # Obstaculo
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
