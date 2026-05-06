from .Cell import Cell

DIRECTIONS = {
        Cell.N: (-1, 0),
        Cell.S: (1, 0),
        Cell.E: (0, 1),
        Cell.W: (0, -1)
    }


class Maze():
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[Cell]] = []
