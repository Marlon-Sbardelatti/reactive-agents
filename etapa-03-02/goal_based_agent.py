from typing import List, Tuple
from random import randint


class GoalBasedAgent:
    def __init__(self, grid_size: int, obstacles: List[Tuple]) -> None:
        self.limit = grid_size - 1
        self.directions = ["N", "L", "S", "O"]
        self.memory = []
        self.obstacles = obstacles
        self.is_stuck = False
        self.goal_completed = False

        self.set_positions()

    def set_positions(self):
        self.position = self.create_random_position()

        target = self.create_random_position()
        while target == self.position:
            target = self.create_random_position()

        self.target = target

    def create_random_position(self) -> Tuple:
        x = randint(0, self.limit)
        y = randint(0, self.limit)
        return (x, y)

    def move(self):
        if self.position == self.target:
            self.goal_completed = True
            return

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

        self.position = new_position
        self.memory.append(self.position)

    def get_next_position(self) -> Tuple:
        return tuple((a + b) for a, b in zip(self.position, self.calculate_move()))

    def has_finished(self) -> bool:
        return self.is_stuck or self.goal_completed

    def rotate(self):
        direction = self.directions.pop(0)
        self.directions.append(direction)

    def calculate_move(self) -> Tuple:
        # if self.position[0] < self.target[0]:
        #     return (1, 0)
        # elif self.position[0] > self.target[0]:
        #     return (-1, 0)
        # elif self.position[1] < self.target[1]:
        #     return (0, 1)
        # elif self.position[1] > self.target[1]:
        #     return (0, -1)

        # return (0, 0)
        
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

    def get_results(self) -> str:
        result = "Sim" if self.goal_completed else "Não"
        return f"""
FIM DE JOGO!
Destino alcançado: {result}
Comprimento do caminho: {len(self.memory) - 1}
        """
