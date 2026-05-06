from parser import parser
from Cell import Cell
import random
import sys


Grid = list[list[Cell]]


def display_hex_grid(grid: Grid) -> None:
    for row in grid:
        for cell in row:
            print(f"{cell.convert_walls()}", end="")
        print()


class Maze:
    def __init__(self, width: int, height: int, seed: int):
        self.width = width
        self.height = height
        self.seed = seed

    def grid(self) -> Grid:
        grid = [[Cell() for _ in range(self.width)]
                for _ in range(self.height)]
        return grid

    def draw_maze(self, x, y, grid: Grid):
        grid[y][x].visited = True

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                if not grid[ny][nx].visited:

                    direction = Cell.convert_direction((dx, dy))
                    opposite = Cell.convert_direction((-dx, -dy))

                    grid[y][x].walls &= ~direction
                    grid[ny][nx].walls &= ~opposite

                    self.draw_maze(nx, ny, grid)


def print_maze(maze: Grid) -> None:
    h = len(maze)
    w = len(maze[0])
    WHITE = "\033[47;30m"
    NC = "\033[0m"

    print(f"{WHITE} {NC}" + f"{WHITE}    {NC}" * w)

    for y in range(h):
        line = f"{WHITE} {NC}"
        bottom = f"{WHITE} {NC}"

        for x in range(w):
            cell = maze[y][x]

            line += "   "

            if cell.walls & Cell.E:
                line += f"{WHITE} {NC}"
            else:
                line += " "

            if cell.walls & Cell.S:
                bottom += f"{WHITE}    {NC}"
            else:
                bottom += f"   {WHITE} {NC}"

        print(line)
        print(bottom)


def test() -> None:
    config = parser(sys.argv)
    width = config["WIDTH"]
    height = config["HEIGHT"]

    maze = Maze(width, height, 0)
    grid = maze.grid()
    maze.draw_maze(0, 0, grid)
    display_hex_grid(grid)
    print()
    print_maze(grid)


if __name__ == "__main__":
    test()
