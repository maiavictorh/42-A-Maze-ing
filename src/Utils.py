from abc import ABC, abstractmethod
from typing import Any


GREEN = "\033[92m"
GREEN_BK = "\033[42m"
YELLOW = "\33[1;93m"
YELLOW_BK = "\33[43m"
RED = "\033[31m"
RED_BK = "\033[41;30m"
NC = "\33[0m"
PURPLE_BL = "\33[1;35;5m"
PURPLE = "\33[1;35m"
CLEAR = "\033c"
ROXO = "\033[45;30m"
PURPLE_42 = "\33[48;2;95;0;151m"
WHITE = "\033[47;30m"
GRAY = "\33[3;100m"


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
