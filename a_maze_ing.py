from src import parser, RED, NC, CoordinateError, MazeError
from sys import argv, exit


if __name__ == "__main__":
    try:
        if len(argv) != 2:
            raise ValueError(f"Expected 2 arguments, given: {len(argv)}")

        config = parser(argv)
        print(config)  # TEST

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        exit()
