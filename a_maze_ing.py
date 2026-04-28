from src.get_config import get_config
import random
import sys


def print_maze(maze: list) -> None:
    for row in maze:
        for cell in row:
            if cell == '+':
                sys.stdout.write("\033[40m  \033[0m")
            else:
                sys.stdout.write("\033[47m  \033[0m")
        sys.stdout.write("\n")


def main() -> None:

    config = get_config("config.txt")
    parser_wid = int(config.get("WIDTH"))
    parser_hei = int(config.get("HEIGHT"))
    output_file = config["OUTPUT_FILE"]
    width = parser_wid
    height = parser_hei

    maze = [['0' for _ in range(width)] for _ in range(height)]

    def draw_maze(x: int, y: int) -> None:
        maze[y][x] = '+'
        moves = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(moves)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if nx > 0 and nx < width - 1 and ny > 0 and ny < height - 1:
                if maze[ny][nx] == '0':
                    maze[y + dy//2][x + dx//2] = '+'
                    draw_maze(nx, ny)

    draw_maze(1, 1)
    try:
        with open(output_file, "w") as file:
            for line in maze:
                file.write(f"{''.join(line)}\n")
    except Exception as err:
        print(F"Error: {err}")

    print_maze(maze)


if __name__ == "__main__":
    main()
