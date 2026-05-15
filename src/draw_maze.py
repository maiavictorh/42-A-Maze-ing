from utils import WHITE, NC, PURPLE_42 as P42, GREEN, ROXO, RED_BK
from typing import Optional
from src.Cell import Cell
import random

Grid = list[list[Cell]]

def path(path_config: str, wall_color: str, fill: Optional[str] = "   ") -> str:
    MID_CLOSED = f"{wall_color} {NC}{fill}{wall_color} {NC}"
    MID_OPEN = f" {fill} "
    LEFT_MID_OPEN = f" {fill}{wall_color} {NC}"
    RIGHT_MID_OPEN = f"{wall_color} {NC}{fill} "

    UP_OPEN = f"{wall_color} {NC}   {wall_color} {NC}"
    UP_CLOSED = f"{wall_color}     {NC}"

    DOWN_OPEN = f"{wall_color} {NC}   {wall_color} {NC}"
    DOWN_CLOSED = f"{wall_color}     {NC}"
    CELL42 = f"{wall_color} {NC}{fill}   {NC}{wall_color} {NC}"

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
              show_path: Optional[bool] = False,
              rotate_colors: Optional[bool] = False) -> None:

    N, E, S, W = 1, 2, 4, 8
    ex, ey = entry
    ty, tx = exit

    walls_colors = WHITE
    colors = [GREEN, ROXO, RED_BK]
    if rotate_colors:
        random.shuffle(colors)
        walls_colors = colors[0]

    for x, row in enumerate(grid):  # Loop principal para todas as linhas

        for cell in row:  # Primeiro loop, print so a parte de cima da celula
            print(path("up_closed", walls_colors) if cell.walls & N else path("up_open", walls_colors), end="")
        print()

        for y, cell in enumerate(row):  # Segundo loop, printa o meio da cell

            is_entry = (x == ex and y == ey)
            is_exit = (x == tx and y == ty)

            mid_closed = path("mid_closed", walls_colors)
            mid_open = path("mid_open", walls_colors)
            left_mid_open = path("left_mid_open", walls_colors)
            right_mid_open = path("right_mid_open", walls_colors)

            if show_path and cell.in_path:
                way = f" {GREEN}\33[1m+ "
                mid_closed = path("mid_closed", walls_colors, way)
                mid_open = path("mid_open", walls_colors, way)
                left_mid_open = path("left_mid_open", walls_colors, way)
                right_mid_open = path("right_mid_open", walls_colors, way)

            if is_entry or is_exit:
                door = ROXO if is_entry else RED_BK
                print_door = f" {door} {NC} "

                mid_closed = path("mid_closed", walls_colors, print_door)
                mid_open = path("mid_open", walls_colors, print_door)
                left_mid_open = path("left_mid_open", walls_colors, print_door)
                right_mid_open = path("right_mid_open", walls_colors, print_door)

            left = bool(cell.walls & W)
            right = bool(cell.walls & E)

            if cell.cell42:
                mid_closed = path("cell42", walls_colors, P42)
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
        print(path("down_closed", walls_colors) if cell.walls & S else path("down_open", walls_colors), end="")
    print()
