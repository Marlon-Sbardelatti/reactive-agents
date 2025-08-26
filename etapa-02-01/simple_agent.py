from typing import List, Tuple

class SimpleAgent:
    def __init__(self, grid_size: int, position: Tuple) -> None:
        self.limit = grid_size - 1
        self.position = position
        self.memory = [position]
        self.directions = ["N", "L", "S", "O"]
        self.collided_walls = []
        self.is_stuck = False
        self.goal_completed = False

    def move(self):
        if len(self.memory) == pow(self.limit + 1, 2):
            self.goal_completed = True
            return

        new_position = self.get_next_position()

        available_positions = []
        rotations_made = 0

        while rotations_made < 4:
            if not (self.will_collide() or new_position in self.memory):
                available_positions.append((
                    new_position, tuple((a - b) for a, b in zip(self.position, new_position))
                ))

            self.rotate()
            new_position = self.get_next_position()
            rotations_made += 1

        if not available_positions:
            self.is_stuck = True
            return

        self.position = self.get_best_position(available_positions)
        self.memory.append(self.position)

    def has_finished(self) -> bool:
        return self.is_stuck or self.goal_completed

    def get_next_position(self) -> Tuple:
        return tuple((a + b) for a, b in zip(self.position, self.calculate_move()))

    def get_best_position(self, available_positions: List[Tuple]) -> Tuple:
        """
            Retorna melhor posição vizinha disponível,
            com base na menor distância até uma das bordas
        """
        if not self.at_border():
            return min(
                available_positions,
                key=lambda position: self.distance_to_nearest_border(position[0])
            )[0]
        return self.choose_zigzag_move(available_positions)

    def at_border(self) -> bool:
        """Verifica se o agente está em um dos extremos do grid"""
        x, y = self.position
        return (
            x == 0 or
            y == 0 or
            x == self.limit or
            y == self.limit
        )

    def distance_to_nearest_border(self, position: Tuple) -> int:
        x, y = position
        return min(x, y, self.limit - x, self.limit - y)

    def choose_zigzag_move(self, available_positions):
        x, y = self.position
        

        # Coluna par → desce
        if y % 2 == 0:
            for position, difference in available_positions:
                if difference == (1, 0):
                    return position
            for position, difference in available_positions:
                if difference == (0, 1):
                    return position

        # Coluna ímpar → sobe
        else:
            for position, difference in available_positions:
                if difference == (-1, 0):
                    return position
            for position, difference in available_positions:
                if difference == (0, 1):
                    return position

        return available_positions[0][0]

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
        x, y = self.position

        match self.directions[0]:
            case "N":
                return y == 0
            case "S":
                return y == self.limit
            case "L":
                return x == self.limit
            case "O":
                return x == 0
            case _:
                return False

    def get_results(self) -> str:
        result = "Sim" if self.goal_completed else "Não"
        return f"""
FIM DE JOGO!
Destino alcançado: {result}
Comprimento do caminho: {len(self.memory) - 1}
        """
