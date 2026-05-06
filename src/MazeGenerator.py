from src.parser import parser
from src.Cell import Cell
import random
import sys

DIRS = {
        Cell.N: (-1, 0),
        Cell.S: (1, 0),
        Cell.E: (0, 1),
        Cell.W: (0, -1)
    }

class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height


    def gen_maze(self) -> list[list[Cell]]:
        gride = [[Cell() for _ in range(self.width)]
                 for _ in range(self.height)]

        def draw(r, c):
            gride[r][c].visited = True

            directions = list(MazeGenerator.DIRS.keys())
            random.shuffle(directions)

            for d in directions:
                dx, dy = MazeGenerator.DIRS[d]


def test() -> None:
    config = parser(sys.argv)
    width = config["WIDTH"]
    height = config["HEIGHT"]

    maze = MazeGenerator(width, height)
