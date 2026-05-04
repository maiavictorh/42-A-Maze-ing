from .parser import parser
from .Utils import CoordinateError, MazeError, GREEN, RED, NC

__errors__ = [CoordinateError, MazeError]
__functions__ = [parser]
__colors__ = [GREEN, RED, NC]
