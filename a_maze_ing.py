from src import parser, MazeGenerator
from utils import MazeError, CoordinateError
import sys


def user_interactions():
    print("\n=== A-Maze-ing ===")
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
            # Gererate new maze
            print("TEST")
        case 2:
            # Show/Hide path from entry to exit
            print("TEST")
        case 3:
            # Rotate maze colors
            print("TEST")
        case 4:
            print(YELLOW, "Quitting...", NC)
            sys.exit()


if __name__ == "__main__":
    GREEN = "\33[92m"
    YELLOW = "\33[93m"
    RED = "\33[31m"
    NC = "\33[0m"

    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Expected 2 arguments, given: {len(sys.argv)}")

        config = parser(sys.argv)
        maze = MazeGenerator(config).generate()

        user_interactions()

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        sys.exit()
