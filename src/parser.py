from typing import Any
from utils.Processor import Processor
from utils import MazeError, CoordinateError
from utils import NumericProcessor, CoordinateProcessor, \
                    TextProcessor, ConditionProcessor


def parser(args: list[str]) -> dict[str, Any]:
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
            key = key.strip()
            value = value.strip()
            if key not in validators:
                raise KeyError(f"Unknown key: {key}")
            if key in config:
                raise KeyError("No duplicated config allowed")
            config[key] = validators[key].converter(value)

        for k in validators:
            if k not in config:
                raise KeyError(f"Missing parameter: {k}")

        if config['WIDTH'] < 5 or config['HEIGHT'] < 5:
            raise MazeError("Maze is too small, mininum: 5x5")

        if config['ENTRY'] == config['EXIT']:
            raise CoordinateError("Entry and Exit must be different")

        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]
        if entry_x >= config["WIDTH"] or entry_y >= config["HEIGHT"]:
            raise CoordinateError("Entry must be inside the Maze")
        if exit_x >= config["WIDTH"] or exit_y >= config["HEIGHT"]:
            raise CoordinateError("Exit must be inside the Maze")

    return config
