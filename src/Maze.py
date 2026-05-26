from .Utils import CoordinateError


class Cell:
    """
    Represents a single maze cell with four possible walls.

    A cell behaves like a block containing four walls
    (North, East, South, and West), represented internally
    as a nibble (four bits). If a wall is closed, its bit is
    set to ``1``; if it is open, the bit is set to ``0``,
    indicating that movement is allowed in that direction.

    The North wall is represented by the least significant bit (LSB).

    By default, a cell starts with all walls closed:

        1111  -> 15 (decimal)

    The walls can be opened using bitwise operations.

    Example:
        Opening the North wall:

            walls = 15 = 1111
            N     =  1 = 0001
           ~N     = ~1 = 1110

            walls &= ~N

        Result:

            1110 -> 14 (decimal) -> E (hexadecimal)

    Attributes:
        walls (int): Bitmask representing the current wall configuration.
        visited (bool): Indicates whether the cell has already been visited.
        cell42 (bool): Marks the cell as part of the decorative "42" pattern.
        in_path (bool): Indicates whether the cell belongs to the solution
        path.
    """

    N, E, S, W = 1, 2, 4, 8

    def __init__(self) -> None:
        self.walls = 15
        self.visited = False
        self.cell42 = False
        self.in_path = False

    def convert_walls(self) -> str:
        """
        Convert the wall bitmask into a hexadecimal representation.

        Returns:
            str: Hexadecimal character corresponding to the current
            wall configuration.
        """

        return "0123456789ABCDEF"[self.walls]

    @staticmethod
    def convert_direction(coordinate: tuple[int, int]) -> int:
        """
        Convert a coordinate offset into a directional constant.

        Args:
            coordinate (tuple[int, int]):
                Coordinate offset representing a direction.

                Supported values:

                - ``(0, -1)`` -> North
                - ``(1, 0)`` -> East
                - ``(0, 1)`` -> South
                - ``(-1, 0)`` -> West

        Raises:
            ValueError: If the coordinate does not represent
                a valid direction.

        Returns:
            int: Direction constant defined by ``Cell``.
        """

        if coordinate == (0, -1):
            return Cell.N
        if coordinate == (1, 0):
            return Cell.E
        if coordinate == (0, 1):
            return Cell.S
        if coordinate == (-1, 0):
            return Cell.W
        raise ValueError("Invalid Coordinate")


class Maze:
    """
    Represents a maze based on a two-dimensional grid of cells.

    This class is resposabible for creating and managing a matrix of
    "Cell" objects, as well as providing utilities for coordinate
    validation, neighbor retrivial, and path storage.

    Attributes:
        width (int): Width of the maze in number of cells.
        height (int): Height of the maze in number of cells.
        seed (int): Value used for randomness control.
        grid (list[list[Cell]]): Matrix containing the maze cells.
        path (list[tuple[int, int]]): Stored path represented as coordinates
        pairs.
    """
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[Cell]] = self.create_grid()
        self.path: list[tuple[int, int]] = []

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Check whether a coordinate is inside maze boundaries.

        Args:
            x (int): Horizontal coordinate.
            y (int): Vertical coordinate.

        Returs:
            bool: "True" if the coordinate is valid, otherwise "False".
        """

        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Returns the cell located at a specific coordinate.

        Args:
            x (int): Horizontal cell coordinate.
            y (int): Vertical cell coordinate.

        Raises:
            CoordinateError: If the coordinate is outside maze boundaries.

        Returns:
            Cell: The Cell object located  at the given position.
        """

        if not self.in_bounds(x, y):
            raise CoordinateError("Couldn't reach Cell: Out of bounds")
        return self.grid[y][x]

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int, int]]:
        """
        Retrieve valid neighboring cells for a valid position.

        Returned directions use the identifiers defined by the
        "Cell" class.

        Args:
            x (int): Horizontal cell coordinate.
            y (int): Vertical cell coordinate.

        Returns:
            list[tuple[int, int, int]]:
                A list of tuples in the format
                (direction, nx, ny), where:
                - direction is the neighbor direction.
                - nx is the horizontal coordinate.
                - ny is the vertical coordinate:
        """

        neighbors: list[tuple[int, int, int]] = []

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
        """
        Create and initializate the maze grid.

        The grid is composed of "Cell" objects arranged in a
        two-dimensional matrix. If the maze  dimensions are larger
        than 8x8, a visual pattern representation of the number 42
        is draw using the "cell42" property.

        Returns:
            list[list[Cell]]: Matrix containing all created cells.
        """

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
