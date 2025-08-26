from typing import List, Tuple
from random import randint


class ModelBasedAgent:
    def __init__(self, grid_size: int, obstacles: List[Tuple]) -> None:
        self.limit = grid_size - 1
        self.position = self.calculate_initial_position()
        self.directions = ["N", "L", "S", "O"]
        self.collided_walls = []
        self.memory = []
        self.obstacles = obstacles
        self.goal_completed = False
        self.is_stuck = False

    def calculate_initial_position(self) -> Tuple:
        x = randint(0, self.limit)
        y = randint(0, self.limit)
        return (x, y)

    def move(self):
        new_position = self.get_next_position()
        rotations_made = 0

        while (
            self.will_collide()
            or new_position in self.memory
            or new_position in self.obstacles
        ):
            if rotations_made >= 4:
                self.is_stuck = True
                return

            self.rotate()
            rotations_made += 1
            new_position = self.get_next_position()

        self.position = self.get_next_position()
        self.memory.append(self.position)

    def get_next_position(self) -> Tuple:
        return tuple((a + b) for a, b in zip(self.position, self.calculate_move()))

    def verify_goal_completed(self) -> bool:
        if self.directions[0] not in self.collided_walls:
            self.collided_walls.append(self.directions[0])

        return len(self.collided_walls) == 4

    def calculate_move(self) -> Tuple:
        match self.directions[0]:
            case "N":
                return (0, -1)
            case "S":
                return (0, 1)
            case "L":
                return (1, 0)
            case "O":
                return (-1, 0)
            case _:
                return (0, 0)

    def rotate(self):
        direction = self.directions.pop(0)
        self.directions.append(direction)

    def will_collide(self) -> bool:
        match self.directions[0]:
            case "N":
                return self.position[1] == 0
            case "S":
                return self.position[1] == self.limit
            case "L":
                return self.position[0] == self.limit
            case "O":
                return self.position[0] == 0
            case _:
                return False

    def has_finished(self) -> bool:
        return self.is_stuck or self.goal_completed

    def get_results(self) -> str:
        total_visitadas = len(self.memory)
        total_casas = pow(self.limit + 1, 2) - len(self.obstacles)
        percentual = (total_visitadas / total_casas) * 100
        if percentual == 100.00:
            self.goal_completed = True
        return f"""
FIM DE JOGO!
Objetivo concluido: {self.goal_completed}
Percentual visitado: {percentual:.2f}%
        """
