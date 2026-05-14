from utils import WHITE, NC, PURPLE_42 as P42, GREEN, RED, ROXO
from typing import Optional
from src.Cell import Cell

Grid = list[list[Cell]]

def path(path_config: str, fill: Optional[str] = "   ") -> str:
    MID_CLOSED = f"{WHITE} {NC}{fill}{WHITE} {NC}"
    MID_OPEN = f" {fill} "
    LEFT_MID_OPEN = f" {fill}{WHITE} {NC}"
    RIGHT_MID_OPEN = f"{WHITE} {NC}{fill} "

    UP_OPEN = f"{WHITE} {NC}   {WHITE} {NC}"
    UP_CLOSED = f"{WHITE}     {NC}"

    DOWN_OPEN = f"{WHITE} {NC}   {WHITE} {NC}"
    DOWN_CLOSED = f"{WHITE}     {NC}"
    CELL42 = f"{WHITE} {NC}{fill}   {NC}{WHITE} {NC}"

    walls = {
        "mid_closed": MID_CLOSED,
        "mid_open": MID_OPEN,
        "left_mid_open": LEFT_MID_OPEN,
        "right_mid_open": RIGHT_MID_OPEN,
        "up_open": UP_OPEN,
        "up_closed": UP_CLOSED,
        "down_open": DOWN_OPEN,
        "down_closed": DOWN_CLOSED,
        "cell42": CELL42
    }
    return walls[path_config]


def draw_maze(grid: Grid, entry: tuple, exit: tuple,
              show_path: Optional[bool] = False) -> None:

    N, E, S, W = 1, 2, 4, 8
    ex, ey = entry
    ty, tx = exit

    for x, row in enumerate(grid):  # Loop principal para todas as linhas

        for cell in row:  # Primeiro loop, print so a parte de cima da celula
            print(path("up_closed") if cell.walls & N else path("up_open"), end="")
        print()

        for y, cell in enumerate(row):  # Segundo loop, printa o meio da cell

            is_entry = (x == ex and y == ey)
            is_exit = (x == tx and y == ty)

            mid_closed = path("mid_closed")
            mid_open = path("mid_open")
            left_mid_open = path("left_mid_open")
            right_mid_open = path("right_mid_open")

            if show_path and cell.in_path:
                way = f" {GREEN} {NC} "
                mid_closed = path("mid_closed", way)
                mid_open = path("mid_open", way)
                left_mid_open = path("left_mid_open", way)
                right_mid_open = path("right_mid_open", way)

            if is_entry or is_exit:
                door = ROXO if is_entry else RED
                print_door = f" {door} {NC} "

                mid_closed = path("mid_closed", print_door)
                mid_open = path("mid_open", print_door)
                left_mid_open = path("left_mid_open", print_door)
                right_mid_open = path("right_mid_open", print_door)

            left = bool(cell.walls & W)
            right = bool(cell.walls & E)

            if cell.cell42:
                mid_closed = path("cell42", P42)
            if left and right:
                print(mid_closed, end="")
            elif left and not right:
                print(right_mid_open, end="")
            elif not left and right:
                print(left_mid_open, end="")
            else:
                print(mid_open, end="")
        print()

    for cell in grid[-1]:
        print(path("down_closed") if cell.walls & S else path("down_open"), end="")
    print()
