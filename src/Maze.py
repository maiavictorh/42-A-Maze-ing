from .Cell import Cell
from utils import CoordinateError
from random import Random
from typing import Any

Grid = list[list[Cell]]

DIRECTIONS = {
        Cell.N: (0, -1),
        Cell.S: (0, 1),
        Cell.E: (1, 0),
        Cell.W: (-1, 0)}


class Maze:
    def __init__(self, width: int, height: int, seed: int):
        self.width = width
        self.height = height
        self.seed = Random(seed)
        self.grid = self.create_grid()

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        if not self.in_bounds(x, y):
            raise CoordinateError("Couldn't reach Cell: Out of bounds")
        return self.grid[y][x]

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        neighbors = []

        for direction, (dx, dy) in DIRECTIONS.items():
            nx = x + dx
            ny = y + dy

            if self.in_bounds(nx, ny):
                neighbors.append((direction, nx, ny))
        return neighbors

    def inside_42_cell(self, config: dict[str, Any]) -> bool:
        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        entry_cell = self.get_cell(entry_x, entry_y)
        exit_cell = self.get_cell(exit_x, exit_y)

        if entry_cell.cell42 or exit_cell.cell42:
            return False
        return True

    def create_grid(self) -> Grid:
        grid = [[Cell() for _ in range(self.width)]
                for _ in range(self.height)]

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        four_width = half_width - 3
        four_height = half_height - 2

        two_width = four_width + 4
        two_height = four_height

        # mark 4
        if self.width > 8 and self.height > 8:
            for i in range(2):
                grid[four_height][four_width].cell42 = True
                four_height += 1
            for i in range(2):
                grid[four_height][four_width].cell42 = True
                four_width += 1
            for i in range(2):
                grid[four_height][four_width].cell42 = True
                four_height -= 1
            for i in range(5):
                grid[four_height][four_width].cell42 = True
                four_height += 1

            # mark 2
            for i in range(2):
                grid[two_height][two_width].cell42 = True
                two_width += 1
            for i in range(2):
                grid[two_height][two_width].cell42 = True
                two_height += 1
            for i in range(2):
                grid[two_height][two_width].cell42 = True
                two_width -= 1
            for i in range(2):
                grid[two_height][two_width].cell42 = True
                two_height += 1
            for i in range(3):
                grid[two_height][two_width].cell42 = True
                two_width += 1

        return grid

    def broke_walls(self, x: int, y: int, exit_x: int, exit_y: int) -> bool:
        current = self.grid[y][x]
        current.visited = True

        found_exit = (x == exit_x and y == exit_y)

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.seed.shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if not self.in_bounds(nx, ny):
                continue

            neighbor = self.grid[ny][nx]

            if neighbor.visited or neighbor.cell42:
                continue

            direction = Cell.convert_direction((dx, dy))
            opposite = Cell.convert_direction((-dx, -dy))

            current.walls &= ~direction
            neighbor.walls &= ~opposite

            if self.broke_walls(nx, ny, exit_x, exit_y):
                found_exit = True

        if found_exit:
            current.in_path = True

        return found_exit
