from abc import ABC, abstractmethod
from typing import Any

GREEN = "\33[32m"
RED = "\33[31m"
NC = "\33[0m"


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
            raise ValueError("Config must not be negative")
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
