import sys
from mazegen import parser, MazeGenerator
from mazegen.Utils import MazeError, CoordinateError, RED, EXIT, NC


def main() -> None:
    try:
        config = parser(sys.argv)
        maze_gen = MazeGenerator(config)
        maze_gen.run()

    except (ValueError, KeyError, CoordinateError,
            MazeError, FileNotFoundError, PermissionError, Exception) as err:
        print(f"{RED}Error: {err}\n  {EXIT}Aborting...  {NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
