class Cell:
    N = 1  # -> 0001
    E = 2  # -> 0010
    S = 4  # -> 0100
    W = 8  # -> 1000
    def __init__(self) -> None:
        self.walls = 0
        self.visited = False

    def convert_walls(self):
        return "0123456789ABCDEF"[self.walls]

    @staticmethod
    def convert_direction(cord: tuple[int, int]) -> int:
        if cord == (-1, 0):
            return Cell.N
        if cord == (0, 1):
            return Cell.E
        if cord == (1, 0):
            return Cell.S
        if cord == (0, -1):
            return Cell.W

def check_walls(grid: list[list[Cell]]):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W
    rows, cols = len(grid), len(grid[0])

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny].visited:
                        cell.walls |= cell.convert_direction((dx, dy))


def display_grid(grid: list[list[Cell]]) -> None:
    for row in grid:
        for cell in row:
            if not cell.visited:
                print("0", end="")
            else:
                print(f"{cell.convert_walls()}", end="")
        print()

# TEST
def main() -> None:
    x, y = 5, 5
    grid = [[Cell() for _ in range(x)] for _ in range(y)]
    grid[2][2].visited = True

    grid[1][2].visited = True
    grid[3][2].visited = True
    grid[2][1].visited = True
    grid[2][3].visited = True
    check_walls(grid)
    display_grid(grid)


if __name__ == "__main__":
    main()
