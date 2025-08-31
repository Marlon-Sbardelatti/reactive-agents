from typing import List, Optional, Tuple


class GoalBasedAgent:
    def __init__(self, grid_size: int, initial_position: Tuple) -> None:
        self.limit = grid_size - 1
        self.position = initial_position
        self.memory = [initial_position]
        self.visit_count = {initial_position: 1}
        self.directions = ["N", "L", "S", "O"]
        self.goal_completed = False

    def set_target(self, position: Tuple):
        self.target = position

    def move(self):
        if self.position == self.target:
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
        return tuple((a + b) for a, b in zip(self.position, self.calculate_move()))

    def calculate_move(self) -> Tuple:
        if self.position[0] < self.target[0]:
            return (1, 0)
        elif self.position[0] > self.target[0]:
            return (-1, 0)
        elif self.position[1] < self.target[1]:
            return (0, 1)
        elif self.position[1] > self.target[1]:
            return (0, -1)

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
        return self.goal_completed

    def get_results(self) -> str:
        result = "Sim" if self.goal_completed else "Não"
        return f"""
FIM DE JOGO!
Destino alcançado: {result}
Comprimento do caminho: {len(self.memory) - 1}
        """
