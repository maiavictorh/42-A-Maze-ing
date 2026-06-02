from typing import Any
from .Utils import Processor, NumericProcessor, CoordinateProcessor, \
                    TextProcessor, ConditionProcessor, MazeError, \
                    CoordinateError


def parser(args: list[str]) -> dict[str, Any]:
    """
    Parse and validate a maze configuration file.

    Reads a plain-text configuration file whose path is given as the
    second element of args. Each non-comment, non-empty line must
    follow the KEY=VALUE format. All six mandatory keys must be
    present exactly once, and their values must pass type and semantic
    validation before the config is returned.

    The following keys are mandatory:

    - WIDTH        — maze width in cells (integer ≥ 3).
    - HEIGHT       — maze height in cells (integer ≥ 3).
    - ENTRY        — entry coordinates as x,y (inside bounds).
    - EXIT         — exit coordinates as x,y (inside bounds, ≠ ENTRY).
    - OUTPUT_FILE  — output filename (must end in '.txt').
    - PERFECT      — whether the maze is perfect (True or False).

    Args:
        args: Command-line argument list. args[1] must be the path
            to the configuration file.
    Returns:
        A dictionary mapping each validated key to its converted value:
        "WIDTH" and "HEIGHT" as 'int', "ENTRY" and "EXIT" as
        'tuple[int, int]', "OUTPUT_FILE" as 'str', and "PERFECT"
        as 'bool'.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If a line is not in 'KEY=VALUE' format, the output
            file does not end in '.txt', or a value fails type conversion.
        KeyError: If an unknown key is found, a key appears more than once,
            or a mandatory key is missing.
        CoordinateError: If "ENTRY" equals "EXIT", or either coordinate
            falls outside the maze bounds.
        MazeError: If "WIDTH" or "HEIGHT" is less than 3.
    """
    validators: dict[str, Processor] = {
            "WIDTH": NumericProcessor(),
            "HEIGHT": NumericProcessor(),
            "ENTRY": CoordinateProcessor(),
            "EXIT": CoordinateProcessor(),
            "OUTPUT_FILE": TextProcessor(),
            "PERFECT": ConditionProcessor()
            }

    file_name = args[1]
    with open(file_name, "r") as file:
        config: dict[str, Any] = {}

        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            elif "=" not in line:
                raise ValueError("Invalid format")

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            if key not in validators:
                raise KeyError(f"Unknown key: {key}")
            if key in config:
                raise KeyError("No duplicated config allowed")
            config[key] = validators[key].converter(value)

        for k in validators:
            if k not in config:
                raise KeyError(f"Missing parameter: {k}")

        if config['WIDTH'] < 3 or config['HEIGHT'] < 3:
            raise MazeError("Maze is too small, mininum: 3x3")

        if config['ENTRY'] == config['EXIT']:
            raise CoordinateError("Entry and Exit must be different")

        if ".txt" not in config["OUTPUT_FILE"]:
            raise ValueError("Invalid output file name: must be .txt format")

        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        if entry_x >= config["WIDTH"] or entry_y >= config["HEIGHT"]:
            raise CoordinateError("Entry must be inside the Maze")
        if exit_x >= config["WIDTH"] or exit_y >= config["HEIGHT"]:
            raise CoordinateError("Exit must be inside the Maze")

    return config
