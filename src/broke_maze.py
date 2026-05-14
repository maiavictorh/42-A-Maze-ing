from .Cell import Cell
Grid = list[list[Cell]]
import random


def broke_maze(maze: Grid) -> None:
    for x, row in enumerate(maze):

        for y, cell in enumerate(row):

            if not cell.cell42 and x != 0 and y != len(maze) and y != 0 and x != len(row):
                bits_on = [i for i in range(4) if cell.walls & (1 << i)]

                if bits_on:
                    bit = random.choice(bits_on)
                    cell.walls &= ~(1 << bit)
