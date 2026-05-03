from abc import ABC, abstractmethod
from sys import exit
from typing import Any

GREEN = "\33[32m"
RED = "\33[31m"
NC = "\33[0m"


class Processor(ABC):
    @abstractmethod
    def converter(self, value: str) -> Any:
        pass

    @staticmethod
    def validate_int(value: str) -> int:
        new_value = int(value)
        if new_value < 0:
            raise ValueError("No negative input!")
        return new_value


class NumericProcessor(Processor):
    def converter(self, value: str) -> int:
        return self.validate_int(value)


class TextProcessor(Processor):
    def converter(self, value: str) -> str:
        if not isinstance(value,  str) or len(value) == 0:
            raise ValueError("No empty input!")
        return value


class CoordinateProcessor(Processor):
    def converter(self, value: str) -> tuple[int, int]:
        if "," not in value:
            raise ValueError("Invalid coordinate")
        x, y = value.split(",", 1)
        return self.validate_int(x), self.validate_int(y)


class ConditionProcessor(Processor):
    def converter(self, value: str) -> bool:
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        raise ValueError("Invalid configuration")


def parser(args: list[str]) -> dict:
    validators: dict[str, Processor] = {
            "WIDTH": NumericProcessor(),
            "HEIGHT": NumericProcessor(),
            "ENTRY": CoordinateProcessor(),
            "EXIT": CoordinateProcessor(),
            "OUTPUT_FILE": TextProcessor(),
            "PERFECT": ConditionProcessor()}

    if len(args) != 2:
        raise ValueError(f"Error: Expected 2 arguments, given: {len(args)}")

    file_name = args[1]
    try:
        with open(file_name, "r") as file:
            config: dict[str, Any] = {}

            for line in file:
                line = line.strip()
                if not line or "=" not in line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key not in validators.keys():
                    raise KeyError(f"Unknow key: {key}")
                config[key] = validators[key].converter(value)

            for k in validators.keys():
                if k not in config.keys():
                    raise KeyError(f"Missing parameter: {k}")
            if config['ENTRY'] == config['EXIT']:
                raise ValueError("Entry and Exit must be different")
            if config['WIDTH'] < 1 or config['HEIGHT'] < 1 \
                    or config["WIDTH"] < 2 and config["HEIGHT"] < 2:
                raise ValueError("Maze dimensions must be at least 2x1 or 1x2")

        return config
    except (ValueError, KeyError, FileNotFoundError) as err:
        print(RED, err, NC)
        exit()
