from goal_based_agent import GoalBasedAgent
from typing import Tuple
from random import randint
import time


def main():
    is_default = int(input("Opções de mapa\n1 - Padrão\n2 - Aleatório\nEscolha: "))
    
    if is_default == 1:
        grid_size = 10
        initial_position = (0, 0)
        target = (7,7)
    else:
        grid_size = int(input("Escolha o tamanho do tabuleiro: "))
        
        initial_position = generate_random_position(grid_size)
        target = generate_random_position(grid_size)

        while target == initial_position:
            target = generate_random_position(grid_size)

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
   
    agent = GoalBasedAgent(grid_size, initial_position) 
    agent.set_target(target)

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


def generate_random_position(grid_size) -> Tuple:
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return (x, y)


def get_cell_value(row: int, clmn: int, agent: GoalBasedAgent) -> str:
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
