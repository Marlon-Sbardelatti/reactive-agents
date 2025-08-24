from typing import List, Tuple
import heapq


class UtilityBasedAgent:
    def __init__(self, grid_size: int, grid_weights: List, position: Tuple) -> None:
        self.limit = grid_size - 1
        self.position = position
        self.directions = ["N", "L", "S", "O"]
        self.memory = [position]
        self.is_stuck = False
        self.goal_completed = False
        self.grid_weights = grid_weights

    def set_target(self, position: Tuple):
        self.target = position
        self.best_path = self.dijkstra(self.grid_weights, self.position, self.target)

    def move(self):
        if self.position == self.target:
            self.goal_completed = True
            return

        if self.best_path:
            self.position = self.best_path.pop()
            self.memory.append(self.position)

    def get_best_position(self, available_positions: List[Tuple]) -> Tuple:
        min = ((), 4)

        for p, w in available_positions:
            if w < min[1]:
                min = (p, w)

        return min[0]

    def get_next_position(self) -> Tuple:
        # print(self.position, self.calculate_move(), self.directions[0])
        return tuple((a + b) for a, b in zip(self.position, self.calculate_move()))

    def has_finished(self) -> bool:
        return self.is_stuck or self.goal_completed

    def rotate(self):
        direction = self.directions.pop(0)
        self.directions.append(direction)

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

    def dijkstra(self, grid_weights, start, target):
        rows, cols = len(grid_weights), len(grid_weights[0])
        distances = {(r, c): float("inf") for r in range(rows) for c in range(cols)}
        previous = {(r, c): None for r in range(rows) for c in range(cols)}

        distances[start] = 0
        queue = [(0, start)]

        while queue:
            current_dist, current = heapq.heappop(queue)

            if current == target:
                break

            r, c = current
            neighbors = [
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1),
            ]

            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_dist = current_dist + grid_weights[nr][nc]
                    if new_dist < distances[(nr, nc)]:
                        distances[(nr, nc)] = new_dist
                        previous[(nr, nc)] = current
                        heapq.heappush(queue, (new_dist, (nr, nc)))

        path = []
        cell = target
        while cell is not None:
            path.append(cell)
            cell = previous[cell]

        path.pop()
        return path

    def get_results(self) -> str:
        result = "Sim" if self.goal_completed else "Não"
        total = 0

        for p in self.memory:
            total += self.grid_weights[p[0]][p[1]]

        return f"""
FIM DE JOGO!
Destino alcançado: {result}
Comprimento do caminho: {len(self.memory) - 1}
Custo total: {total}
        """
