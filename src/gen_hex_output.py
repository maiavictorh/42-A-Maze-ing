from .Cell import Cell
Grid = list[list[Cell]]


def gen_hex_output(maze: Grid, output_name: str) -> None:
    try:
        with open(output_name, "w") as file:
            for row in maze:
                for cell in row:
                    file.write(cell.convert_walls())
                file.write("\n")
    except Exception:
        raise
