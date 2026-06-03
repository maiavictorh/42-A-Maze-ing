from sys import exit
from typing import Any
from .Maze import Cell, Maze
from .MazeSolver import MazeSolver
from .MazeRenderer import MazeRenderer
from random import randint, shuffle, choice
from .Utils import (MazeError, CLEAR, NC, PURPLE as P, YELLOW, GREEN_BACK,
                    PURPLE_BACK, RED_BACK, YELLOW_BACK, GRAY_BACK, BLUE_BACK,
                    OCEAN)


class MazeGenerator:
    """
    Orchestrates maze generation, solving, rendering, and export.

    Reads a validated configuration, generates a random maze using an
    iterative DFS algorithm, solves it with BFS, renders it to the
    terminal, and exports it to a file. Provides an interactive menu
    for re-generation and display options.

    Attributes:
        width (int): Maze width in cells.
        height (int): Maze height in cells.
        entry (tuple[int, int]): Entry cell coordinates (x, y).
        exit (tuple[int, int]): Exit cell coordinates (x, y).
        output_file (str): Path to the hexadecimal output file.
        perfect (bool): Whether the maze has a single solution path.
        seed (int): Random seed used for maze generation.
        show_path (bool): Whether the solution path is currently visible.
        rotate_colors (bool): Whether custom wall colors are active.
        current_colors (tuple[str, str] | None): Active (walls, 42)
            ANSI color pair, or None when rotation is off.
        maze (Maze): The currently generated maze instance.
    """
    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialize the generator from a validated configuration dict.

        Args:
            config: Dictionary produced by parser(). Must contain
                "WIDTH", "HEIGHT", "ENTRY", "EXIT",
                "OUTPUT_FILE", and "PERFECT".
        """
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]
        self.seed = randint(1, 999)
        self.show_path = False
        self.rotate_colors = False
        self.current_colors: Any = None
        self.maze = self._generate()

    def run(self) -> None:
        """
        Start the interactive maze loop.

        Clears the terminal, renders the current maze, exports it to
        the output file, and presents a menu. Loops until the user
        chooses to quit.

        Menu options:

        - 1 — Re-generate a new maze.
        - 2 — Toggle the solution path display.
        - 3 — Toggle custom wall color rotation.
        - 4 — Quit the program.

        Raises:
            Exception: Propagates any unexpected error with context.
        """
        try:
            while True:
                print(CLEAR, end="")

                renderer = MazeRenderer(self.maze)

                maze_solver = MazeSolver(self.maze)
                self.maze.path = maze_solver.solve(self.entry, self.exit)

                renderer.render(self.entry, self.exit,
                                self.show_path, self.rotate_colors,
                                self.current_colors)
                renderer.export(self.output_file, self.entry, self.exit)

                print()
                if self.width > 127:
                    print(YELLOW, "Warning: Maze visualization (ASCII) is"
                          " compromised due to it's dimensions!"
                          " Max width recommended: 127", NC)
                if self.width < 9 or self.height < 9:
                    print(YELLOW, "Warning: 42 Pattern visualization is "
                          "compromised due to Maze's dimensions!"
                          " Min recommended: 9x9", NC)
                print()
                print("   ╔════════════════════════════════╗")
                print(f"   ║           \33[3m{P}A-Maze-ing{NC}           ║")
                print("   ║   1. Re-generate a new maze    ║")
                print("   ║   2. Show/Hide path            ║")
                print("   ║   3. Rotate maze colors        ║")
                print("   ║   4. Quit                      ║")
                print("   ╚════════════════════════════════╝")

                match int(input("\n     Choice? (1-4): ")):
                    case 1:
                        self.maze = self._generate()
                    case 2:
                        self.switch_show_path()
                    case 3:
                        self.switch_rotate_colors()
                    case 4:
                        print(YELLOW, "Quitting...", NC)
                        exit()
        except Exception as err:
            raise Exception(f"MazeGenerator: run {err}")

    def switch_show_path(self) -> None:
        """Toggle the visibility of the solution path."""
        self.show_path = not self.show_path

    def switch_rotate_colors(self) -> None:
        """
        Toggle custom wall color rotation.

        When enabled, picks a new random color pair via
        _pick_new_colors. When disabled, resets
        current_colors to None.
        """
        self.rotate_colors = not self.rotate_colors
        if self.rotate_colors:
            self._pick_new_colors()
        else:
            self.current_colors = None

    def _pick_new_colors(self) -> None:
        """
        Select a random pair of distinct ANSI colors for the maze walls.

        Picks two different colors from the available palette and stores
        them in current_colors as a (walls_color, 42_color) tuple.
        """
        colors = [GREEN_BACK, PURPLE_BACK, RED_BACK,
                  YELLOW_BACK, GRAY_BACK, BLUE_BACK, OCEAN]
        walls = choice(colors)
        c42 = choice(colors)
        while c42 == walls:
            c42 = choice(colors)
        self.current_colors = (walls, c42)

    def _generate(self) -> Maze:
        """
        Generate and return a new maze.

        Creates a fresh Maze, validates that neither entry nor exit
        falls inside the "42" pattern, carves passages with the iterative
        DFS algorithm, and optionally breaks random walls for imperfect
        mazes (two passes when self.perfect is False).

        Returns:
            A fully generated Maze instance.
        Raises:
            MazeError: If entry or exit is positioned inside a "42" cell.
        """
        maze = Maze(self.width, self.height, self.seed)

        if self._inside_42_cell(maze):
            raise MazeError("Entry/Exit cannot be inside 42 pattern")

        x, y = self.entry
        exit_x, exit_y = self.exit
        self._carve_passages_iterative(maze, x, y)

        if not self.perfect:
            self._break_random_walls(maze)
            self._break_random_walls(maze)

        return maze

    def _inside_42_cell(self, maze: Maze) -> bool:
        """
        Check whether entry or exit overlaps with the "42" pattern.

        Args:
            maze: The maze whose grid is inspected.
        Returns:
            True if either the entry or exit cell has cell42 set,
            False otherwise.
        """
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        entry_cell = maze.get_cell(entry_x, entry_y)
        exit_cell = maze.get_cell(exit_x, exit_y)
        return (entry_cell.cell42 or exit_cell.cell42)

    def _break_random_walls(self, maze: Maze) -> None:
        """
        Remove one random north wall per row to create maze loops.

        For each row, collects all eligible interior cells — those not
        part of the "42" pattern, not on the border, and whose northern
        neighbor is also not part of "42" — then randomly opens the north
        wall of one such cell (and the corresponding south wall of its
        neighbor above), introducing a loop into the maze.

        Args:
            maze: The maze to modify in place.
        """
        for y, row in enumerate(maze.grid):
            valid_cells: list[tuple[int, Cell]] = []

            for x, cell in enumerate(row):
                if (
                    not cell.cell42
                    and y > 0
                    and y < self.height - 1
                    and x > 0
                    and x < self.width - 1
                    and not maze.grid[y - 1][x].cell42
                ):
                    valid_cells.append((x, cell))

            if valid_cells:
                x, cell = choice(valid_cells)
                cell.walls &= ~Cell.N
                if y > 0:
                    maze.grid[y - 1][x].walls &= ~Cell.S

    def _carve_passages_iterative(self,
                                  maze: Maze,
                                  start_x: int,
                                  start_y: int) -> None:
        """
        Carve maze passages using an iterative DFS with backtracking.

        Starting from (start_x, start_y), explores the grid by
        randomly shuffling available directions at each step and carving
        walls between the current cell and unvisited, non "42" neighbors.
        Uses an explicit stack to avoid Python's recursion limit.

        Each stack frame stores (x, y, moves, i), where moves is
        the shuffled direction list and 'i' is the index of the next
        direction to try. When all directions are exhausted, the frame is
        popped (backtrack).

        Args:
            maze: The maze whose walls will be carved in place.
            start_x: Horizontal coordinate of the starting cell.
            start_y: Vertical coordinate of the starting cell.
        """

        stack = []

        maze.grid[start_y][start_x].visited = True

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        shuffle(moves)

        stack.append((start_x, start_y, moves, 0))

        while stack:
            x, y, moves, i = stack[-1]
            current: Cell = maze.grid[y][x]

            if i >= len(moves):
                stack.pop()
                continue

            stack[-1] = (x, y, moves, i + 1)

            dx, dy = moves[i]
            nx, ny = x + dx, y + dy

            if not maze.in_bounds(nx, ny):
                continue

            neighbor = maze.grid[ny][nx]

            if neighbor.visited or neighbor.cell42:
                continue

            neighbor.visited = True

            direction = Cell.convert_direction((dx, dy))
            opposite = Cell.convert_direction((-dx, -dy))

            current.walls &= ~direction
            neighbor.walls &= ~opposite

            next_moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            shuffle(next_moves)

            stack.append((nx, ny, next_moves, 0))
