class Cell:
    """
        A cell is like a square with four walls (N, E, S, W), wich is
    represented as a nibble (0000), if the wall is closed the bit is set
    to '1', '0' means there is a path in that direction. The north
    is set to the LSB.
        The cell starts with all walls closed (1111), which is the value 15 in
    decimal.
        The principal idea is to set the N which is the lsb to the value 1
    wich is 0001, and use the bitwise operation: walls &= ~N.
        ex:
            walls = 15 = 1111
            N     = 1  = 0001
           ~N     =~1  = 1110
            &  15 & ~1 = 1110
        now the variable wall is 14, or E in hexa.
    """
    N = 1  # -> ~1110
    E = 2  # -> ~1101
    S = 4  # -> ~1011
    W = 8  # -> ~0111

    def __init__(self) -> None:
        self.walls = 15
        self.visited = False
        self.cell42 = False

    def convert_walls(self) -> str:
        return "0123456789ABCDEF"[self.walls]

    @staticmethod
    def convert_direction(cord: tuple[int, int]) -> int:
        """
        Return the directin of the given coordenate.

        """
        if cord == (0, -1):
            return Cell.N
        if cord == (1, 0):
            return Cell.E
        if cord == (0, 1):
            return Cell.S
        if cord == (-1, 0):
            return Cell.W
        raise ValueError("Cell Error: Invalid Coordenate")
