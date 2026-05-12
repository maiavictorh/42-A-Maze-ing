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

    N, E, S, W = 1, 2, 4, 8

    def __init__(self) -> None:
        self.walls = 15
        self.visited = False  # TEST
        self.cell42 = False

    def convert_walls(self) -> str:
        return "0123456789ABCDEF"[self.walls]

    @staticmethod
    def convert_direction(cord: tuple[int, int]) -> int:
        """
        Return the direction of the given coordenate.
        """
        if cord == (0, -1):
            return Cell.N
        if cord == (1, 0):
            return Cell.E
        if cord == (0, 1):
            return Cell.S
        if cord == (-1, 0):
            return Cell.W
        raise ValueError("Invalid Coordinate")
