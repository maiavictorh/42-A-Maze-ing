from typing import Optional
from .Maze import Maze
from .Utils import WHITE_BACK, RED_BACK, PURPLE_42 as P42, \
                    GREEN_BACK, ENTRY, EXIT, PURPLE_BLINK, \
                    YELLOW_BLINK, GREEN, NC


class MazeRenderer:
    """
    Handles terminal rendering and file export of a maze.

    Provides two independent responsibilities: printing an ASCII
    representation of the maze to the terminal using ANSI color codes,
    and writing the maze's hexadecimal wall encoding plus solution path
    to an output file.

    Attributes:
        maze (Maze): The maze instance to render and export.
    """
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def render(self, entry: tuple[int, int], exit: tuple[int, int],
               show_path: Optional[bool] = False,
               rotate_colors: Optional[bool] = False,
               current_colors: Optional[tuple[str, str]] = None) -> None:
        """
        Print the maze to the terminal as an ASCII representation.

        Iterates over every row of the grid twice: once to print each
        cell's north wall, and once to print its middle section
        (left wall, interior, right wall). After all rows, the south
        walls of the last row are printed. Entry and exit cells are
        highlighted with blinking colored block characters. Cells on
        the solution path are marked with a • dot when
        show_path is True. Cells that belong to the "42"
        pattern are filled with a colored background.

        Wall and "42" colors adapt automatically when rotate_colors
        is active and a current_colors pair is provided. Entry and
        exit colors also adjust to maintain contrast against the active
        wall color.

        Args:
            entry: Entry cell coordinates (x, y).
            exit: Exit cell coordinates (x, y).
            show_path: If True, marks solution path cells with
                a green •. Defaults to False.
            rotate_colors: If True, applies current_colors
                instead of the default white walls. Defaults to False.
            current_colors: A (walls_color, 42_color) ANSI string
                pair used when rotate_colors is active. Ignored
                if None or if rotate_colors is False.
        """
        walls_colors = WHITE_BACK
        entry_color = ENTRY
        exit_color = EXIT
        c42_color = P42
        ey, ex = entry
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
        Build an ANSI-colored ASCII segment for a single cell section.

        Looks up the requested segment layout from an internal dictionary
        and interpolates the wall color and fill string into it.

        Available segment configurations:

        - "up_closed"       — top wall, fully closed.
        - "up_open"         — top wall, open (passage above).
        - "down_closed"     — bottom wall, fully closed.
        - "down_open"       — bottom wall, open (passage below).
        - "mid_closed"      — middle row, both left and right walls closed.
        - "mid_open"        — middle row, both left and right walls open.
        - "left_mid_open"   — middle row, left wall open, right wall closed.
        - "right_mid_open"  — middle row, left wall closed, right wall open.
        - "cell42"          — middle row for a "42" pattern cell.

        Args:
            segment_config: Key identifying the desired segment layout.
            wall_color: ANSI escape string applied to wall characters.
            fill: Three-character string printed inside the cell body.
                Defaults to three spaces.
        Returns:
            The fully formatted ANSI string for the requested segment.
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

    def export(self, output_name: str,
               entry: tuple[int, int], exit: tuple[int, int]) -> None:
        """
        Write the maze to a file in hexadecimal format with solution path.

        Writes the maze grid row by row, one hexadecimal character per
        cell, followed by an empty line, the entry coordinates, the exit
        coordinates, and the shortest path encoded as a sequence of
        cardinal direction letters (N, E, S, W).

        Output file structure::

            <hex_row_0>
            <hex_row_1>
            ...
            <hex_row_n>

            <entry>
            <exit>
            <NESW...>

        Args:
            output_name: Path to the output file. Created or overwritten.
            entry: Entry cell coordinates (x, y).
            exit: Exit cell coordinates (x, y).
        Raises:
            Exception: Propagates any file I/O error encountered during
                writing.
        """
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
