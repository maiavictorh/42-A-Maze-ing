class Cell:
    """
    A Cell is like a block with four walls (N, E, S, W), which is
    represented as a nibble (four bits). If the wall is closed, the bit is set
    to '1', if it's open, the bit is set to '0', meaning there is a path
    in that direction. The North is set to the LSB (Less Significant Bit).

    The cell starts with all walls closed (1111), which is 15 in
    decimal.

    The main idea is to set the North to 1 (0001), and use the bitwise
    operation: walls &= ~N.
    ex:
        walls = 15 = 1111
        N     =  1 = 0001
       ~N     = ~1 = 1110

    Now the wall's value is 14, or E in hexa.
    """
    N = 1  # -> ~1110
    E = 2  # -> ~1101
    S = 4  # -> ~1011
    W = 8  # -> ~0111

    def __init__(self) -> None:
        self.walls = 15
        self.visited = False  # TEST

    def convert_walls(self) -> str:
        return "0123456789ABCDEF"[self.walls]


def convert_direction(cord: tuple[int, int]) -> int:
    """
    Return the direction of the given coordenate.
    """
    if cord == (-1, 0):
        return Cell.N
    if cord == (0, 1):
        return Cell.E
    if cord == (1, 0):
        return Cell.S
    if cord == (0, -1):
        return Cell.W
    raise ValueError("Invalid Coordinate")


def check_walls(grid: list[list[Cell]]) -> None:
    """
    Check all the cells in the grid.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W
    rows, cols = len(grid), len(grid[0])

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny].visited:
                        direction = convert_direction((dx, dy))
                        cell.walls &= ~direction

                        opposite = convert_direction((-dx, -dy))
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
    # grid[2][2].visited = True
    grid[0][0].visited = True
    grid[2][0].visited = True

    check_walls(grid)
    display_grid(grid)


if __name__ == "__main__":
    main()
