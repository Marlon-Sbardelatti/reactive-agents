from typing import Tuple


class SimpleAgent:
    def __init__(self, grid_size: int, initial_position: Tuple) -> None:
        self.limit = grid_size - 1
        self.position = initial_position
        self.directions = ["N", "L", "S", "O"]
        self.collided_walls = []
        self.goal_completed = False

    def move(self):
        rotations_made = 0

        while self.will_collide():
            if self.verify_goal_completed():
                self.goal_completed = True
                break

            self.rotate()
            rotations_made += 1

        if rotations_made >= 4:
            return

        self.position = tuple(
            (a + b) for a, b in zip(self.position, self.calculate_move())
        )

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

    def get_results(self) -> str:
        result = "Sim" if self.goal_completed else "Não"

        return f"""
FIM DE JOGO!
Destino alcançado: {result}
            """
