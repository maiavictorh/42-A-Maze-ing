from typing import Optional
from .Maze import Maze
from .Utils import WHITE_BACK, RED_BACK, PURPLE_42 as P42, \
                    GREEN_BACK, ENTRY, EXIT, PURPLE_BLINK, \
                    YELLOW_BLINK, GREEN, NC


class MazeRenderer:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    # RENDERER - Prints on terminal the representation of the maze.

    def render(self, entry: tuple[int, int], exit: tuple[int, int],
               show_path: Optional[bool] = False,
               rotate_colors: Optional[bool] = False,
               current_colors: Optional[tuple[str, str]] = None) -> None:

        walls_colors = WHITE_BACK
        entry_color = ENTRY
        exit_color = EXIT
        c42_color = P42
        ex, ey = entry
        ty, tx = exit

        if rotate_colors and current_colors is not None:
            walls_colors, c42_color = current_colors
        if walls_colors == GREEN_BACK:
            entry_color = PURPLE_BLINK
        if walls_colors == RED_BACK:
            exit_color = YELLOW_BLINK

        for x, row in enumerate(self.maze.grid):  # Print all the lines
            for cell in row:  # Prints the upper wall of the cell
                print(self._wall_segment("up_closed", walls_colors)
                      if cell.walls & 1 else
                      self._wall_segment("up_open", walls_colors), end="")
            print()

            for y, cell in enumerate(row):  # Prints the middle of the cell

                is_entry = (x == ex and y == ey)
                is_exit = (x == tx and y == ty)
                inside_cell = "   "

                if show_path and cell.in_path:
                    inside_cell = f" {GREEN}• "

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

        for cell in self.maze.grid[-1]:  # Prints the last row's walls
            print(self._wall_segment("down_closed", walls_colors)
                  if cell.walls & 4 else
                  self._wall_segment("down_open", walls_colors), end="")

        print()

    @staticmethod
    def _wall_segment(segment_config: str, wall_color: str,
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

    # EXPORTER - Writes the maze in hexadecimal in a file.

    def export(self, output_name: str,
               entry: tuple[int, int], exit: tuple[int, int]) -> None:
        dirs = {
            (0, -1): "N",
            (1, 0): "E",
            (0, 1): "S",
            (-1, 0): "W"
        }
        try:
            with open(output_name, "w") as file:
                for row in self.maze.grid:
                    for cell in row:
                        file.write(cell.convert_walls())
                    file.write("\n")

                file.write(f"\n{str(entry)}\n{str(exit)}\n")

                for direction in self.maze.path:
                    file.write(f"{dirs[direction]}")

        except Exception:
            raise
