from .Utils import WHITE_BACK, PURPLE_BACK, RED_BACK, PURPLE_42 as P42, \
                    GREEN_BACK, YELLOW_BACK, ENTRY, EXIT, PURPLE_BLINK, \
                    YELLOW_BLINK
from .Utils import CoordinateError
from random import Random, choice
from typing import Any, Optional
from .Utils import NC, GREEN
from .Cell import Cell


class Maze:
    def __init__(self, width: int, height: int, seed: int):
        self.width = width
        self.height = height
        self.seed = Random(seed)
        self.grid: list[list[Cell]] = self.create_grid()
        self.path: list[tuple[int, int]] = []

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        if not self._in_bounds(x, y):
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

            if self._in_bounds(nx, ny):
                neighbors.append((direction, nx, ny))
        return neighbors

    def inside_42_cell(self, config: dict[str, Any]) -> bool:
        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        entry_cell = self.get_cell(entry_x, entry_y)
        exit_cell = self.get_cell(exit_x, exit_y)

        if entry_cell.cell42 or exit_cell.cell42:
            return False
        return True

    def create_grid(self) -> list[list[Cell]]:
        grid = [[Cell() for _ in range(self.width)]
                for _ in range(self.height)]

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        four_width = half_width - 3
        four_height = half_height - 2

        two_width = four_width + 4
        two_height = four_height

        # mark 4
        if self.width > 8 and self.height > 8:
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

    def broke_walls(self, x: int, y: int, exit_x: int, exit_y: int) -> bool:
        current = self.grid[y][x]
        current.visited = True

        found_exit = (x == exit_x and y == exit_y)

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.seed.shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if not self._in_bounds(nx, ny):
                continue

            neighbor = self.grid[ny][nx]

            if neighbor.visited or neighbor.cell42:
                continue

            direction = Cell.convert_direction((dx, dy))
            opposite = Cell.convert_direction((-dx, -dy))

            current.walls &= ~direction
            neighbor.walls &= ~opposite

            if self.broke_walls(nx, ny, exit_x, exit_y):

                self.path.append((dx, dy))
                found_exit = True

        if found_exit:
            current.in_path = True

        return found_exit

    def broke_maze(self) -> None:
        for x, row in enumerate(self.grid):
            valid_cells: list[tuple[int, Cell]] = []

            for y, cell in enumerate(row):
                if (
                    not cell.cell42
                    and x > 0
                    and x < self.height - 1
                    and y > 0
                    and y < self.width - 1
                    and not self.grid[x][y - 1].cell42
                ):
                    valid_cells.append((y, cell))

            if valid_cells:
                y, cell = self.seed.choice(valid_cells)
                cell.walls &= ~Cell.N
                if x > 0:
                    self.grid[x - 1][y].walls &= ~Cell.S

    def gen_hex_output(self, output_name: str,
                       entry: tuple, exit: tuple) -> None:
        dirs = {
            (0, -1): "N",
            (1, 0): "E",
            (0, 1): "S",
            (-1, 0): "W"
        }

        try:
            with open(output_name, "w") as file:
                for row in self.grid:

                    for cell in row:
                        file.write(cell.convert_walls())
                    file.write("\n")

                file.write(f"\n{str(entry)}\n{str(exit)}\n")

                self.path.reverse()

                for direction in self.path:
                    file.write(f"{dirs[direction]}")

        except Exception:
            raise

    def draw_maze(self, entry: tuple, exit: tuple,
                  show_path: Optional[bool] = False,
                  rotate_colors: Optional[bool] = False) -> None:

        colors = [GREEN_BACK, PURPLE_BACK, RED_BACK, YELLOW_BACK]
        walls_colors = WHITE_BACK
        entry_color = ENTRY
        exit_color = EXIT
        c42_color = P42
        ex, ey = entry
        ty, tx = exit

        if rotate_colors:
            walls_colors = choice(colors)
            c42_color = choice(colors)
            while c42_color == walls_colors:
                c42_color = choice(colors)
            if walls_colors == GREEN_BACK:
                entry_color = PURPLE_BLINK
            if walls_colors == RED_BACK:
                exit_color = YELLOW_BLINK

        for x, row in enumerate(self.grid):  # Main loop, print all the lines
            for cell in row:  # First loop, prints the upper wall of the cell
                print(self._wall_segment("up_closed", walls_colors)
                      if cell.walls & 1 else
                      self._wall_segment("up_open", walls_colors), end="")
            print()

            for y, cell in enumerate(row):  # Prints the middle of the cell

                is_entry = (x == ex and y == ey)
                is_exit = (x == tx and y == ty)
                inside_cell = "   "

                if show_path and cell.in_path:
                    inside_cell = f" {GREEN}\33[1m+ "

                if is_entry or is_exit:
                    door = entry_color if is_entry else exit_color
                    inside_cell = f" {door}█{NC} "

                elif cell.cell42:
                    inside_cell = f"{c42_color}   {NC}"

                mid_closed = self._wall_segment("mid_closed", walls_colors,
                                                inside_cell)
                mid_open = self._wall_segment("mid_open", walls_colors,
                                              inside_cell)
                left_mid_open = self._wall_segment("left_mid_open",
                                                   walls_colors, inside_cell)
                right_mid_open = self._wall_segment("right_mid_open",
                                                    walls_colors, inside_cell)

                left = bool(cell.walls & 8)
                right = bool(cell.walls & 2)

                if left and right:
                    print(mid_closed, end="")
                elif left and not right:
                    print(right_mid_open, end="")
                elif not left and right:
                    print(left_mid_open, end="")
                else:
                    print(mid_open, end="")
            print()

        for cell in self.grid[-1]:  # Prints the last row's walls
            print(self._wall_segment("down_closed", walls_colors)
                  if cell.walls & 4 else
                  self._wall_segment("down_open", walls_colors), end="")

        print()

    def _wall_segment(self, segment_config: str, wall_color: str,
                      fill: Optional[str] = "   ") -> str:
        """
        Returns the ascii segment corresponding to the requested configuration.
        """
        segment = {
            "mid_closed": f"{wall_color}▒{NC}{fill}{wall_color} {NC}",
            "mid_open": f" {fill} ",
            "left_mid_open": f" {fill}{wall_color} {NC}",
            "right_mid_open": f"{wall_color}▒{NC}{fill} ",
            "up_open": f"{wall_color}▒{NC}   {wall_color} {NC}",
            "up_closed": f"{wall_color}     {NC}",
            "down_open": f"{wall_color} {NC}   {wall_color}▒{NC}",
            "down_closed": f"{wall_color}     {NC}",
            "cell42": f"{wall_color} {NC}{fill}   {NC}{wall_color} {NC}"
        }
        return segment[segment_config]
