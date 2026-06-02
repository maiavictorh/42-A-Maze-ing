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

RED_BACK = "\33[41;30m"
GREEN_BACK = "\33[42;30m"
YELLOW_BACK = "\33[43;30m"
BLUE_BACK = "\33[44;30m"
PURPLE_BACK = "\33[45;30m"
OCEAN = "\33[46;30m"
WHITE_BACK = "\33[47;30m"
GRAY_BACK = "\33[100;30m"

NC = "\33[0m"
CLEAR = "\033c"


class MazeError(Exception):
    """Custom Exception for maze related errors"""
    pass


class CoordinateError(MazeError):
    """Custom Exception for coordinate related errors"""
    pass


class Processor(ABC):
    """
    Abstract base class for configuration value processors.

    Subclasses must implement the 'converter' method to parse
    and validate a raw string value from the configuration file.
    """
    @abstractmethod
    def converter(self, value: str) -> Any:
        """
        Convert a raw string value into the appropriate type.

        Args:
            value: Raw string extracted from the configuration file.
        Returns:
            The converted value in the expected type.
        Raises:
            ValueError: If the value cannot be converted or is invalid.
        """
        pass

    @staticmethod
    def validate_int(value: str) -> int:
        """
        Parse a string as a non-negative integer.

        Args:
            value: String representation of an integer.
        Returns:
            The parsed non-negative integer.
        Raises:
            ValueError: If the string is not a valid integer or is negative.
        """
        new_value = int(value)
        if new_value < 0:
            raise ValueError("Config cannot be negative")
        return new_value


class NumericProcessor(Processor):
    """Processor for integer configuration values."""
    def converter(self, value: str) -> int:
        """
        Convert a string to a non-negative integer.

        Args:
            value: String representation of an integer.
        Returns:
            The parsed non-negative integer.
        Raises:
            ValueError: If the value is negative or not an integer.
        """
        return self.validate_int(value)


class TextProcessor(Processor):
    """Processor for non-empty string configuration values."""
    def converter(self, value: str) -> str:
        """
        Validate and return a non-empty string.

        Args:
            value: Raw string from the configuration file.
        Returns:
            The original string if valid.
        Raises:
            ValueError: If the value is empty or is not a string.
        """
        if len(value.strip()) == 0:
            raise ValueError("Config must not be empty")
        return value


class CoordinateProcessor(Processor):
    """Processor for coordinate configuration values in x,y format."""
    def converter(self, value: str) -> tuple[int, int]:
        """
        Convert a 'x,y' string into a tuple of non-negative integers.

        Args:
            value: Coordinate string in the format "x,y".
        Returns:
            A tuple (x, y) of non-negative integers.
        Raises:
            ValueError: If the format is invalid or any component is negative.
        """
        if "," not in value:
            raise ValueError("Invalid coordinate")
        x, y = value.split(",", 1)
        return self.validate_int(x), self.validate_int(y)


class ConditionProcessor(Processor):
    """Processor for boolean configuration values."""
    def converter(self, value: str) -> bool:
        """
        Convert a "true" or "false" string to a boolean.

        Args:
            value: Case-insensitive string representation of a boolean.
        Returns:
            True if the value is "true", False if "false".
        Raises:
            ValueError: If the value is neither "true" nor "false".
        """
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        raise ValueError("Invalid configuration")
