from .Cell import Cell
from utils import CoordinateError
from random import shuffle

Grid = list[list[Cell]]


class Maze2:
    def __init__(self, width: int, height: int, seed: int):
        self.width = width
        self.height = height
        self.seed = seed

    def grid(self) -> Grid:
        grid = [[Cell() for _ in range(self.width)]
                for _ in range(self.height)]

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        four_width = half_width - 2
        four_height = half_height - 2

        two_width = four_width + 4
        two_height = four_height

        # mark 4
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

    def broke_walls(self, x: int, y: int, grid: Grid):
        grid[y][x].visited = True

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                if not grid[ny][nx].visited and not grid[ny][nx].cell42:

                    direction = Cell.convert_direction((dx, dy))
                    opposite = Cell.convert_direction((-dx, -dy))

                    grid[y][x].walls &= ~direction
                    grid[ny][nx].walls &= ~opposite

                    self.broke_walls(nx, ny, grid)


DIRECTIONS = {
        Cell.N: (0, -1),
        Cell.S: (0, 1),
        Cell.E: (1, 0),
        Cell.W: (-1, 0)}


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
