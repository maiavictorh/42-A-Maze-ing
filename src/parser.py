from .Utils import Processor, NumericProcessor, CoordinateProcessor, \
                    TextProcessor, ConditionProcessor
from .Utils import MazeError, CoordinateError
from typing import Any


def validate_parser(validators: dict[str, Processor],
                    config: dict[str, Any]) -> None:
    for k in validators:
        if k not in config:
            raise KeyError(f"Missing parameter: {k}")

    if config['WIDTH'] < 1 or config['HEIGHT'] < 1 \
            or config["WIDTH"] < 2 and config["HEIGHT"] < 2:
        raise MazeError("Maze dimensions must be at least 2x1 or 1x2")

    if config['ENTRY'] == config['EXIT']:
        raise CoordinateError("Entry and Exit must be different")

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]
    if entry_x > config["WIDTH"] or entry_y > config["HEIGHT"]:
        raise CoordinateError("Entry must be inside the Maze")
    if exit_x > config["WIDTH"] or exit_y > config["HEIGHT"]:
        raise CoordinateError("Exit must be inside the Maze")


def parser(args: list[str]) -> dict:
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
            if not line or "=" not in line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key not in validators:
                raise KeyError(f"Unknown key: {key}")
            if key in config:
                raise KeyError("No duplicated keys allowed")
            config[key] = validators[key].converter(value)

        validate_parser(validators, config)

    return config
