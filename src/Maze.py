from .Cell import Cell
import random


class Maze:

    DIRECTIONS = {
        Cell.N: (-1, 0),
        Cell.S: (1, 0),
        Cell.E: (0, 1),
        Cell.W: (0, -1)
    }

    def __init__(self, height: int, width: int) -> None:
        self.height = self.__validate(height)
        self.width = self.__validate(width)

    @staticmethod
    def __validate(value: int) -> int:
        if value < 0 or not isinstance(value, int):
            return 0
        return value

    def gen_maze(self) -> None:
        gride = [[Cell() for i in range(self.width)]
                 for i in range(self.height)]

        def draw(r, c):
            gride[r][c].visited = True

            directions = list(Maze.DIRS.keys())
            random.shuffle(directions)

            for d in directions:
                dx, dy = Maze.DIRS[d]
