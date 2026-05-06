from .Maze import Maze
from typing import Any


class MazeGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]

    def generate(self) -> Maze:
        return Maze(self.width, self.height, self.entry, self.exit)
