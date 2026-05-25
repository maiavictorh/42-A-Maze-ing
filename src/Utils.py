from abc import ABC, abstractmethod
from typing import Any


RED = "\033[31m"
GREEN = "\033[92m"
YELLOW = "\33[93m"
PURPLE = "\33[1;35m"
PURPLE_42 = "\33[48;2;95;0;151m"

ENTRY = "\33[5;32m"
EXIT = "\33[5;31m"
PURPLE_BLINK = "\33[1;35;5m"
YELLOW_BLINK = "\33[5;93m"
WHITE_BLINK = "\33[5m"

YELLOW_BACK = "\33[43m"
RED_BACK = "\033[41;30m"
PURPLE_BACK = "\033[45;30m"
WHITE_BACK = "\033[47;30m"
GREEN_BACK = "\033[42m"
GRAY_BACK = "\33[100m"

NC = "\33[0m"
CLEAR = "\033c"


class MazeError(Exception):
    pass


class CoordinateError(MazeError):
    pass


class Processor(ABC):
    @abstractmethod
    def converter(self, value: str) -> Any:
        pass

    @staticmethod
    def validate_int(value: str) -> int:
        new_value = int(value)
        if new_value < 0:
            raise ValueError("Config cannot be negative")
        return new_value


class NumericProcessor(Processor):
    def converter(self, value: str) -> int:
        return self.validate_int(value)


class TextProcessor(Processor):
    def converter(self, value: str) -> str:
        if not isinstance(value,  str) or len(value) == 0:
            raise ValueError("Config must not be empty")
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
