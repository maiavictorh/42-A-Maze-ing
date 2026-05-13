from src.Cell import Cell
from utils import WHITE, NC, PURPLE_42 as P42

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

            if cell.cell42:
                MID_CLOSED = f"{WHITE} {NC}{P42}   {NC}{WHITE} {NC}"
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
