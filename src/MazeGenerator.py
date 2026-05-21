from sys import exit
from typing import Any
from random import randint, shuffle, choice
from .Maze import Cell, Maze
from .MazeRenderer import MazeRenderer
from .Utils import (MazeError, CLEAR, NC,
                    PURPLE as P, YELLOW)


class MazeGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]
        self.seed = randint(1, 999)
        self.show_path = False
        self.rotate_colors = False
        self.maze = self._generate()

    def run(self) -> None:
        while True:
            print(CLEAR, end="")
            renderer = MazeRenderer(self.maze)
            renderer.draw_maze(self.entry, self.exit,
                               self.show_path, self.rotate_colors)
            renderer.gen_hex_output(self.output_file, self.entry, self.exit)

            options = [
                "Re-generate a new maze",
                "Show/Hide path from entry to exit",
                "Rotate maze colors",
                "Quit"
            ]
            print(f"\n{P}==={NC} {P}A-Maze-ing{NC} {P}==={NC}")
            for i, opt in enumerate(options, start=1):
                print(f"{i}. {opt}")
            match int(input("Choice? (1-4): ")):
                case 1:
                    self.maze = self._generate()
                case 2:
                    self.switch_show_path()
                case 3:
                    self.switch_rotate_colors()
                case 4:
                    print(YELLOW, "Quitting...", NC)
                    exit()

    def switch_show_path(self) -> None:
        self.show_path = not self.show_path

    def switch_rotate_colors(self) -> None:
        self.rotate_colors = not self.rotate_colors

    def _generate(self) -> Maze:
        maze = Maze(self.width, self.height, self.seed)

        if not self._inside_42_cell(maze):
            raise MazeError("Entry/Exit cannot be inside 42 pattern")

        x, y = self.entry
        exit_x, exit_y = self.exit
        self._broke_walls(maze, x, y, exit_x, exit_y)

        if not self.perfect:
            self._broke_maze(maze)

        return maze

    def _inside_42_cell(self, maze: Maze) -> bool:
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        entry_cell = maze.get_cell(entry_x, entry_y)
        exit_cell = maze.get_cell(exit_x, exit_y)
        if not entry_cell.cell42 or exit_cell.cell42:
            return True
        return False

    def _broke_walls(self, maze: Maze,
                     x: int, y: int,
                     exit_x: int, exit_y: int) -> bool:
        current = maze.grid[y][x]
        current.visited = True

        found_exit = (x == exit_x and y == exit_y)

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if not maze._in_bounds(nx, ny):
                continue

            neighbor = maze.grid[ny][nx]

            if neighbor.visited or neighbor.cell42:
                continue

            direction = Cell.convert_direction((dx, dy))
            opposite = Cell.convert_direction((-dx, -dy))

            current.walls &= ~direction
            neighbor.walls &= ~opposite

            if self._broke_walls(maze, nx, ny, exit_x, exit_y):
                maze.path.append((dx, dy))
                found_exit = True

        if found_exit:
            current.in_path = True

        return found_exit

    def _broke_maze(self, maze: Maze) -> None:
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
