from src import parser, MazeGenerator
from utils import MazeError, CoordinateError
import sys


if __name__ == "__main__":
    GREEN = "\33[32m"
    RED = "\33[31m"
    NC = "\33[0m"

    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Expected 2 arguments, given: {len(sys.argv)}")

        config = parser(sys.argv)
        maze_gen = MazeGenerator(config)
        maze = maze_gen.generate()

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        sys.exit()
