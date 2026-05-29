from collections import deque
from .Maze import Maze, Cell


class MazeSolver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def solve(self, entry: tuple[int, int],
              exit: tuple[int, int]) -> list[tuple[int, int]]:

        queue = deque([entry])

        visited = set()
        visited.add(entry)

        parent = {}

        directions = {
            Cell.N: (0, -1),
            Cell.S: (0, 1),
            Cell.E: (1, 0),
            Cell.W: (-1, 0)
        }

        while queue:
            x, y = queue.popleft()

            if (x, y) == exit:
                break

            current = self.maze.get_cell(x, y)

            for direction, (dx, dy) in directions.items():

                if current.walls & direction:
                    continue

                nx = x + dx
                ny = y + dy

                if not self.maze.in_bounds(nx, ny):
                    continue

                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))

                parent[(nx, ny)] = (x, y)

                queue.append((nx, ny))

        path = []
        moves = []

        if exit not in parent and exit != entry:
            return []

        node = exit

        while node != entry:

            path.append(node)

            px, py = parent[node]
            nx, ny = node

            dx = nx - px
            dy = ny - py

            moves.append((dx, dy))

            node = parent[node]

        path.append(entry)
        path.reverse()
        moves.reverse()

        for x, y in path:
            self.maze.get_cell(x, y).in_path = True

        return moves
