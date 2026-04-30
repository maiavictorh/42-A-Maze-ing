class Cell:
    N, S, E, W = 1, 2, 4, 8

    def __init__(self) -> None:
        self.walls = 0
        self.visited = False

    def open(self, direction: tuple) -> None:
        self.walls |= direction

    def close(self, direction: tuple) -> None:
        self.walls &= ~direction

    def is_open(self, direction: tuple) -> bool:
        return (self.walls & direction) != 0
