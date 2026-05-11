from .Cell import Cell
from utils import CoordinateError

DIRECTIONS = {
        Cell.N: (0, -1),
        Cell.S: (0, 1),
        Cell.E: (1, 0),
        Cell.W: (-1, 0)
    }


class Maze:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

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
