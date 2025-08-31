from typing import List, Optional, Tuple


class ModelBasedAgent:
    def __init__(self, grid_size: int, initial_position: Tuple) -> None:
        self.limit = grid_size - 1
        self.position = initial_position
        self.memory = [initial_position]
        self.visit_count = {initial_position: 1}
        self.directions = ["N", "L", "S", "O"]
        self.goal_completed = False

    def move(self):
        if len(self.memory) == pow(self.limit + 1, 2):
            self.goal_completed = True
            return

        available_positions = self.get_available_positions()

        if available_positions:
            self.position = self.get_best_position(available_positions)
        else:
            revisitable_positions = self.get_available_positions(True)
            if revisitable_positions:
                self.position = self.get_best_revisit(revisitable_positions)

        if self.position not in self.memory:
            self.memory.append(self.position)

        self.visit_count[self.position] = self.visit_count.get(self.position, 0) + 1


    def get_available_positions(self, revisit: Optional[bool] = False) -> List[Tuple]:
        positions = []
        new_position = self.get_next_position()
        rotations_made = 0

        while rotations_made < 4:
            if not self.will_collide() and (
                revisit or (new_position not in self.memory)
            ):
                positions.append(new_position)

            self.rotate()
            new_position = self.get_next_position()
            rotations_made += 1

        return positions

    def get_best_position(self, available_positions: List[Tuple]) -> Tuple:
        """Escolhe célula inédita mais próxima"""
        return min(available_positions, key=lambda pos: self.distance_to_position(pos))

    def get_best_revisit(self, positions: List[Tuple]) -> Tuple:
        """Escolhe célula revisitada com menos visitas e mais próxima de célula inexplorada"""
        return min(
            positions,
            key=lambda pos: (
                self.visit_count.get(pos, 0),
                self.distance_to_nearest_unvisited(pos),
            ),
        )

    def distance_to_position(self, position: Tuple) -> int:
        """Distância entre posição atual e posição alvo"""
        x, y = self.position
        tx, ty = position
        return abs(x - tx) + abs(y - ty)

    def distance_to_nearest_unvisited(self, position: Tuple) -> int:
        """Distância até célula não visitada mais próxima"""
        x, y = position
        unvisited = {
            (i, j)
            for i in range(self.limit + 1)
            for j in range(self.limit + 1)
            if (i, j) not in self.memory
        }
        if not unvisited:
            return 0
        return min(abs(x - ux) + abs(y - uy) for ux, uy in unvisited)

    def get_next_position(self) -> Tuple:
        return tuple(a + b for a, b in zip(self.position, self.calculate_move()))

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

    def has_finished(self) -> bool:
        return self.goal_completed

    def get_results(self) -> str:
        result = "Sim" if self.goal_completed else "Não"
        repeated_times = 0

        for value in self.visit_count.values():
            if value > 1:
                repeated_times += value

        return f"""
FIM DE JOGO!
Destino alcançado: {result}
Comprimento do caminho: {len(self.memory) - 1}
Número de revisitas: {repeated_times}
        """
