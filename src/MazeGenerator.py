from parser import parser
from Cell import Cell
import random
import sys


WHITE = "\033[47;30m"
NC = "\033[0m"
DOOR = "\033[45;30m"
Grid = list[list[Cell]]


def draw_maze(grid: Grid, entry: tuple, exit: tuple) -> None:
    UP_OPEN = f"{WHITE} {NC}   {WHITE} {NC}"
    UP_CLOSED = f"{WHITE}     {NC}"

    DOWN_OPEN = f"{WHITE} {NC}   {WHITE} {NC}"
    DOWN_CLOSED = f"{WHITE}     {NC}"

    N, E, S, W = 1, 2, 4, 8
    ex, ey = entry
    ty, tx = exit

    for x, row in enumerate(grid):  # Loop principal para todas as linhas

        for cell in row:  # Primeiro loop, print so a parte de cima da celula
            print(UP_CLOSED if cell.walls & N else UP_OPEN, end="")
        print()

        for y, cell in enumerate(row):  # Segundo loop, printa o meio da cell
            MID_CLOSED = f"{WHITE} {NC}   {WHITE} {NC}"
            MID_OPEN = "     "
            LEFT_MID_OPEN = f"    {WHITE} {NC}"
            RIGHT_MID_OPEN = f"{WHITE} {NC}    "
            DOOR = "\033[45;30m"
            if (x == ex and y == ey) or (x == tx and y == ty):
                if x == ex and y == ey:
                    ex, ey = -1, -1
                else:
                    tx, ty = -1, -1
                    DOOR = "\033[41;30m"

                MID_CLOSED = f"{WHITE} {NC} {DOOR} {NC} {WHITE} {NC}"
                MID_OPEN = f"  {DOOR} {NC}  "
                LEFT_MID_OPEN = f"  {DOOR} {NC} {WHITE} {NC}"
                RIGHT_MID_OPEN = f"{WHITE} {NC} {DOOR} {NC}  "

            left = bool(cell.walls & W)
            right = bool(cell.walls & E)

            if left and right:
                print(MID_CLOSED, end="")
            elif left and not right:
                print(RIGHT_MID_OPEN, end="")
            elif not left and right:
                print(LEFT_MID_OPEN, end="")
            else:
                print(MID_OPEN, end="")
        print()

    for cell in grid[-1]:
        print(DOWN_CLOSED if cell.walls & S else DOWN_OPEN, end="")
    print()


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

    def broke_walls(self, x, y, grid: Grid):
        grid[y][x].visited = True

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                if not grid[ny][nx].visited and not grid[ny][nx].cell42:

                    direction = Cell.convert_direction((dx, dy))
                    opposite = Cell.convert_direction((-dx, -dy))

                    grid[y][x].walls &= ~direction
                    grid[ny][nx].walls &= ~opposite

                    self.broke_walls(nx, ny, grid)


def broke_perfect_maze(maze: Grid):
    pass


def test() -> None:
    config = parser(sys.argv)
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit = config["EXIT"]

    maze = Maze(width, height, 0)
    grid = maze.grid()
    maze.broke_walls(0, 0, grid)
    display_hex_grid(grid)
    print()
    draw_maze(grid, entry, exit)


if __name__ == "__main__":
    test()
