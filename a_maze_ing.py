from utils import RED, NC, YELLOW, PURPLE as P, PURPLE_BL as PB, CLEAR
from utils import MazeError, CoordinateError
from src import parser, draw_maze, Maze
from src import gen_hex_output
from src import broke_maze
import random
import sys


def user_interactions(maze: Maze, config: dict) -> None:
    print(f"\n{P}==={NC} {PB}A-Maze-ing{NC} {P}==={NC}")
    options = ["Re-generate a new maze",
               "Show/Hide path from entry to exit",
               "Rotate maze colors", "Quit"]
    i = 1
    for opt in options:
        print(f"{i}. {opt}")
        i += 1

    choice = int(input("Choice? (1-4): "))
    match choice:
        case 1:
            print(CLEAR, end="")
            main()  # Generate new maze
        case 2:
            print(CLEAR, end="")  # Show/Hide path from entry to exit
            draw_maze(maze.grid, config["ENTRY"], config["EXIT"], True)
            user_interactions(maze, config)
        case 3:
            print("TEST")  # Rotate maze colors
        case 4:
            print(YELLOW, "Quitting...", NC)
            sys.exit()


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Expected 2 arguments, given: {len(sys.argv)}")

        config = parser(sys.argv)
        maze = Maze(config["WIDTH"], config["HEIGHT"], 10)

        if not maze.inside_42_cell(config):
            raise MazeError("Entry/Exit cannot be inside 42 pattern")

        x, y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        maze.broke_walls(x, y, exit_x, exit_y)

        if not config["PERFECT"]:
            broke_maze(maze.grid)

        draw_maze(maze.grid, config["ENTRY"], config["EXIT"], False)
        gen_hex_output(maze.grid, "maze.txt")
        user_interactions(maze, config)

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        sys.exit()


if __name__ == "__main__":
    main()
