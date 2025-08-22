from typing import Tuple
from random import randint


class SimpleAgent:
    def __init__(self, grid_size: int) -> None:
        self.limit = grid_size - 1
        self.position = self.calculate_initial_position()
        self.directions = ["N", "L", "S", "O"]
        self.collided_walls = []
        self.memory = []

    def calculate_initial_position(self) -> Tuple:
        x = randint(0, self.limit)
        y = randint(0, self.limit)
        return (x, y)

    def move(self):
        while self.will_collide():
            if self.verify_goal_completed():
                self.position = (-1, -1)  # flag de objetivo completo
                break

            self.rotate()

        if self.position != (-1, -1):
            new_position = self.position = tuple(
                (a + b) for a, b in zip(self.position, self.calculate_move())
            )
            print(new_position)

            if self.check_free_space(new_position):
                self.memory.append(new_position)
            else:
                self.rotate()

        print("fui para:", self.position, "direcao:", self.directions[0])

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

    def check_free_space(self, position: Tuple) -> bool:
        return position not in self.memory

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
