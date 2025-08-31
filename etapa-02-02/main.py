from model_based_agent import ModelBasedAgent
from typing import List, Tuple
from random import randint
import time


def main():
    is_default = int(input("Opções de mapa de obstáculos\n1 - Padrão\n2 - Aleatório\nEscolha: "))
    
    if is_default == 1:
        obstacles = generate_default_obstacles()
        grid_size = 10
    else:
        grid_size = int(input("Escolha o tamanho do tabuleiro: "))
        obstacles = generate_random_obstacles(grid_size)

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
   
    agent = ModelBasedAgent(grid_size, generate_random_position(grid_size), obstacles)

    while not agent.has_finished():
        agent.move()
        time.sleep(1)

        grid = get_updated_grid(agent, grid_size)
        print_grid(grid)

    print(agent.get_results())


def get_updated_grid(agent: ModelBasedAgent, grid_size: int):
    return [
        [get_cell_value(clmn, row, agent) for clmn in range(grid_size)]
        for row in range(grid_size)
    ]
    

def generate_default_obstacles() -> List[Tuple]:
    return [
        (4, 0),
        (0, 1), (3, 1),
        (2, 2), 
        (2, 3), (5, 3),
        (1, 4), (6, 4),
        (3, 5), (5, 5), (6, 5), (7, 5), (8, 5),
        (5, 6), (8, 6),
        (5, 7), (8, 7),
        (5, 8), (7, 8), (8, 8),
        (5, 9)
    ]


def generate_random_obstacles(grid_size: int) -> List[Tuple]:
    obstacles = []

    obstacles_length = randint(1, (pow(grid_size, 2) // 2))

    for _ in range(obstacles_length):
        x = randint(0, grid_size - 1)
        y = randint(0, grid_size - 1)
        obstacles.append((x, y))

    return obstacles


def generate_random_position(grid_size) -> Tuple:
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return (x, y)


def get_cell_value(clmn: int, row: int, agent: ModelBasedAgent) -> str:
    def same_position(cell: Tuple, position: Tuple):
        return cell == position

    current_cell = (clmn, row)

    if same_position(current_cell, agent.position):
        return "♟"  # Player
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
