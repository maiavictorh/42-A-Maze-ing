from sys import exit
from typing import Any
from random import randint, shuffle, choice
from .Maze import Cell, Maze
from .MazeSolver import MazeSolver
from .MazeRenderer import MazeRenderer
from .Utils import (MazeError, CLEAR, NC, PURPLE as P, YELLOW, GREEN_BACK,
                    PURPLE_BACK, RED_BACK, YELLOW_BACK)


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
        self.current_colors: Any = None
        self.maze = self._generate()

    def run(self) -> None:
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
        self.show_path = not self.show_path

    def switch_rotate_colors(self) -> None:
        self.rotate_colors = not self.rotate_colors
        if self.rotate_colors:
            self._pick_new_colors()
        else:
            self.current_colors = None

    def _pick_new_colors(self) -> None:
        colors = [GREEN_BACK, PURPLE_BACK, RED_BACK, YELLOW_BACK]
        walls = choice(colors)
        c42 = choice(colors)
        while c42 == walls:
            c42 = choice(colors)
        self.current_colors = (walls, c42)

    def _generate(self) -> Maze:
        maze = Maze(self.width, self.height, self.seed)

        if not self._inside_42_cell(maze):
            raise MazeError("Entry/Exit cannot be inside 42 pattern")

        x, y = self.entry
        exit_x, exit_y = self.exit
        self._carve_passages_iterative(maze, x, y, exit_x, exit_y)

        if not self.perfect:
            self._break_random_walls(maze)
            self._break_random_walls(maze)

        return maze

    def _inside_42_cell(self, maze: Maze) -> bool:
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        entry_cell = maze.get_cell(entry_x, entry_y)
        exit_cell = maze.get_cell(exit_x, exit_y)
        if not entry_cell.cell42 or exit_cell.cell42:
            return True
        return False

    def _break_random_walls(self, maze: Maze) -> None:
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
                                  start_y: int,
                                  exit_x: int,
                                  exit_y: int) -> bool:

        stack = []

        start = maze.grid[start_y][start_x]
        start.visited = True

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        shuffle(moves)

        stack.append((start_x, start_y, moves, 0))

        found_exit = False

        while stack:
            x, y, moves, i = stack[-1]
            current: Cell = maze.grid[y][x]

            if x == exit_x and y == exit_y:
                found_exit = True

            if i >= len(moves):

                stack.pop()

                if stack and found_exit:
                    px, py, _, _ = stack[-1]

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

        return found_exit
