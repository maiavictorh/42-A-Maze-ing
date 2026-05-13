from src import parser, draw_maze, Maze
from utils import MazeError, CoordinateError
from utils import RED, NC, YELLOW, PURPLE as P, PURPLE_BL as PB, CLEAR
import sys


def user_interactions() -> None:
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
            print("TEST")  # Show/Hide path from entry to exit
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
        maze = Maze(config["WIDTH"], config["HEIGHT"], 0)
        grid = maze.grid

        if not maze.inside_42_cell(config):
            raise MazeError("Entry cannot be inside 42 pattern")

        maze.broke_walls(0, 0, grid)
        draw_maze(grid, config["ENTRY"], config["EXIT"])
        user_interactions()

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        sys.exit()


if __name__ == "__main__":
    main()
