import sys
import random
from src import parser, Maze
from src import RED, NC, YELLOW, PURPLE as P, PURPLE_BLINK as PB, CLEAR, \
                    MazeError, CoordinateError


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Expected 2 arguments, given: {len(sys.argv)}")

        seed = random.randint(1, 999)
        config = parser(sys.argv)
        show_path = False
        rotate_colors = False

        while True:
            maze = Maze(config["WIDTH"], config["HEIGHT"], seed)

            if not maze.inside_42_cell(config):
                raise MazeError("Entry/Exit cannot be inside 42 pattern")

            x, y = config["ENTRY"]
            exit_x, exit_y = config["EXIT"]
            maze.broke_walls(x, y, exit_x, exit_y)

            if not config["PERFECT"]:
                maze.broke_maze()

            print(CLEAR, end="")
            maze.draw_maze(config["ENTRY"], config["EXIT"],
                           show_path, rotate_colors)
            maze.gen_hex_output("maze.txt", config["ENTRY"], config["EXIT"])

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
                    seed = random.randint(1, 999)
                    continue
                case 2:
                    print(CLEAR, end="")
                    show_path = True if not show_path else False

                case 3:
                    print(CLEAR, end="")
                    rotate_colors = True if not rotate_colors else False
                case 4:
                    print(YELLOW, "Quitting...", NC)
                    sys.exit()

    except (ValueError, KeyError, CoordinateError, MazeError,
            FileNotFoundError, PermissionError) as err:
        print(f"{RED}Error: {err}\n  Aborting...  {NC}")
        sys.exit()


if __name__ == "__main__":
    main()
