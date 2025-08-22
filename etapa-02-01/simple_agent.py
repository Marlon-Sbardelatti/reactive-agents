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
        new_position = self.get_next_position()
        print("here: ", new_position)
        # end = False
        count = 0
        while self.will_collide() or new_position in self.memory:
            # print("count", count)
            # if self.its_over():
            #     print("end")
            #     end = True
            if count >= 4:
                self.position = (-1, -1)
                return
            #     break

            self.rotate()
            count += 1
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
