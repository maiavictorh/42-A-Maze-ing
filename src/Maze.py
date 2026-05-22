from .Utils import CoordinateError


class Cell:
    """
    A Cell is like a block with four walls (N, E, S, W), which is
    represented as a nibble (four bits). If the wall is closed, the bit is set
    to '1', if it's open, the bit is set to '0', meaning there is a path
    in that direction. The North is set to the LSB (Less Significant Bit).

    The cell starts with all walls closed (1111), which is 15 in
    decimal.

    The main idea is to set the North to 1 (0001), and use the bitwise
    operation: walls &= ~N.
    ex:
        walls = 15 = 1111
        N     =  1 = 0001
       ~N     = ~1 = 1110

    Now the wall's value is 14, or E in hexa.
    """

    N, E, S, W = 1, 2, 4, 8

    def __init__(self) -> None:
        self.walls = 15
        self.visited = False
        self.cell42 = False
        self.in_path = False

    def convert_walls(self) -> str:
        return "0123456789ABCDEF"[self.walls]

    @staticmethod
    def convert_direction(cord: tuple[int, int]) -> int:
        """Return the direction of the given coordenate."""
        if cord == (0, -1):
            return Cell.N
        if cord == (1, 0):
            return Cell.E
        if cord == (0, 1):
            return Cell.S
        if cord == (-1, 0):
            return Cell.W
        raise ValueError("Invalid Coordinate")


class Maze:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = self.create_grid()
        self.path: list[tuple[int, int]] = []

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        if not self.in_bounds(x, y):
            raise CoordinateError("Couldn't reach Cell: Out of bounds")
        return self.grid[y][x]

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        neighbors = []

        dirs = {
            Cell.N: (0, -1),
            Cell.S: (0, 1),
            Cell.E: (1, 0),
            Cell.W: (-1, 0)
        }

        for direction, (dx, dy) in dirs.items():
            nx = x + dx
            ny = y + dy

            if self.in_bounds(nx, ny):
                neighbors.append((direction, nx, ny))
        return neighbors

    def create_grid(self) -> list[list[Cell]]:
        grid = [[Cell() for _ in range(self.width)]
                for _ in range(self.height)]

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        four_width = half_width - 3
        four_height = half_height - 2

        two_width = four_width + 4
        two_height = four_height

        if self.width > 8 and self.height > 8:
            # Render 4
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

            # Render 2
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
