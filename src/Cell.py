class Cell:
    N = 1  # -> 1110
    E = 2  # -> 1101
    S = 4  # -> 1011
    W = 8  # -> 0111

    def __init__(self) -> None:
        self.walls = 15
        self.visited = False

    def convert_walls(self) -> str:
        return "0123456789ABCDEF"[self.walls]

    @staticmethod
    def convert_direction(cord: tuple[int, int]) -> int:
        """
        Return the directin of the given coordenate.

        """
        if cord == (-1, 0):
            return Cell.N
        if cord == (0, 1):
            return Cell.E
        if cord == (1, 0):
            return Cell.S
        if cord == (0, -1):
            return Cell.W
        raise ValueError("Cell Error: Invalid Coordenate")


def check_directions(grid: list[list[Cell]]):
    """
    Verifies all the cells in the grid.
    Checks all the possible directions in a Cell (N, E, S, W).
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W
    rows, cols = len(grid), len(grid[0])

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny].visited:
                        direction = cell.convert_direction((dx, dy))
                        cell.walls &= ~direction

                        opposite = cell.convert_direction((-dx, -dy))
                        grid[nx][ny].walls &= ~ opposite


# TEST
def display_grid(grid: list[list[Cell]]) -> None:
    for row in grid:
        for cell in row:
            print(f"{cell.convert_walls()}", end="")
        print()


# TEST
def main() -> None:
    x, y = 5, 5
    grid = [[Cell() for _ in range(x)] for _ in range(y)]
    grid[2][2].visited = True
    grid[0][0].visited = True

    check_directions(grid)
    display_grid(grid)


if __name__ == "__main__":
    main()
