from src import parser, RED, NC, CoordinateError, MazeError
import sys


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Expected 2 arguments, given: {len(sys.argv)}")

        config = parser(sys.argv)
        print(config)  # TEST

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        sys.exit()
