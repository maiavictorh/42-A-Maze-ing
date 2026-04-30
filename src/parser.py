from typing import Any
from abc import ABC, abstractmethod


class Processor(ABC):
    @abstractmethod
    def converter(self, value: str) -> Any:
        pass


class NumericProcessor(Processor):
    def converter(self, value: str) -> int:
        return int(value)


class TextProcessor(Processor):
    def converter(self, value: str) -> str:
        if isinstance(value,  str):
            return value


class CordenateProcessor(Processor):
    def converter(self, value: str) -> tuple[int, int]:
        try:
            if "," in value:
                a, b = value.split(",", 1)
                new_value = (int(a), int(b))
                return new_value
        except Exception:
            raise


class ConditionProcessor(Processor):
    def converter(self, value: str) -> bool:
        if value.lower() == "true":
            return True
        else:
            return False


def parser(args: list[str]) -> dict:
    processors = [NumericProcessor(),
                  CordenateProcessor(),
                  ConditionProcessor(),
                  TextProcessor()]

    if len(args) != 2:
        raise ValueError(f"Error: Expecting two arguments, given: {len(args)}")

    file_name = args[1]
    config: dict = {}
    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()

                if not line or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                for process in processors:
                    try:
                        config[key] = process.converter(value)
                        break
                    except Exception:
                        continue

        return config
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception:
        raise
