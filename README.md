*This project has been created as part of the 42 curriculum by victode-, lde-frei.*

# A-Maze-ing

## Description

A-Maze-ing is a terminal based maze generator written in Python. Given a configuration file, the program generates a random maze, optionally perfect (a single unique path between entry and exit), renders it visually in the terminal using ASCII art with ANSI colors, solves it using BFS, and exports the result to a hexadecimal output file.

A notable visual feature: mazes larger than 8×8 cells display the number **"42"** carved into the maze structure using fully closed cells.

**Key features:**
- Iterative DFS-based maze generation with optional imperfection (random wall breaks)
- BFS shortest-path solver
- Full terminal ASCII rendering with customizable wall colors
- Interactive menu: re-generate, toggle solution path, rotate colors
- Hexadecimal export format with entry, exit, and solution path
- Config file parser with full validation
- Reusable `MazeGenerator` class packaged as a pip-installable module

---

## Instructions

### Requirements

- Python 3.10 or later
- `make` (optional but recommended)

### Installation

```bash
git clone git@github.com:maiavictorh/42-A-Maze-ing.git
cd 42-A-Maze-ing
make install
```

This creates a virtual environment and installs all dependencies from `requirements.txt`.

### Running the Program

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Makefile Targets

| Target | Description |
|--------|-------------|
| `make install` | Create virtualenv and install dependencies |
| `make run` | Run the program with `config.txt` |
| `make debug` | Run with Python's `pdb` debugger |
| `make clean` | Remove `__pycache__`, `.mypy_cache`, and virtualenv |
| `make lint` | Run `flake8` + `mypy` with standard flags |
| `make lint-strict` | Run `flake8` + `mypy --strict` |

---

## Configuration File Format

The configuration file contains one `KEY=VALUE` pair per line. Lines beginning with `#` are treated as comments and ignored. All six keys below are **mandatory**.

```
# Example config.txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `WIDTH` | Integer ≥ 3 | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Integer ≥ 3 | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | `x,y` | Entry cell coordinates (0-based) | `ENTRY=0,0` |
| `EXIT` | `x,y` | Exit cell coordinates (0-based) | `EXIT=19,14` |
| `OUTPUT_FILE` | `.txt` filename | Path to the hex output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True`/`False` | Whether the maze has a single solution | `PERFECT=True` |

**Validation rules enforced by the parser:**
- `WIDTH` and `HEIGHT` must be ≥ 3.
- `ENTRY` and `EXIT` must be different and within bounds.
- `OUTPUT_FILE` must end in `.txt`.
- No duplicate or unknown keys are allowed.
- Entry and exit cannot be placed inside the "42" decorative pattern.

---

## Maze Generation Algorithm

The project uses an **iterative DFS (Depth-First Search) with backtracking**, also known as the **Recursive Backtracker algorithm**, implemented iteratively with an explicit stack to avoid Python's recursion limit.

**How it works:**
1. Start from the entry cell, mark it as visited.
2. Push it onto the stack with a shuffled list of 4 directions.
3. At each step, try the next unvisited, non-"42" neighbor.
4. If found, carve the wall between the current cell and the neighbor, mark the neighbor as visited, and push it.
5. If no unvisited neighbor remains, pop the stack (backtrack).
6. Continue until the stack is empty.

**Why this algorithm?**

- **Easy to implement iteratively** — avoids Python's recursion depth limit for large mazes.
- **Produces long, winding corridors** — aesthetically pleasing and challenging mazes.
- **Guarantees connectivity** — every cell is reachable, producing a valid perfect maze by default.
- **Imperfect mode** — after generation, two passes of random wall removal can create loops and multiple paths, controlled by the `PERFECT=False` flag.

---

## Output File Format

The output file stores one hexadecimal digit per cell. Each digit encodes which walls are **closed** as a 4-bit nibble:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 (MSB) | West |

A bit set to `1` means the wall is **closed**; `0` means **open**.

After the grid (one row per line), an empty line separates three additional lines:
1. Entry coordinates `(x, y)`
2. Exit coordinates `(x, y)`
3. Shortest path as a sequence of `N`, `E`, `S`, `W` characters

**Example output:**
```
FEDB...
...
(0, 0)
(19, 14)
EESSSENNE...
```

---

## Reusable Module

The maze generation logic is packaged as a standalone pip-installable Python module located at the root of the repository.

**Package name:** `mazegen-*` (e.g., `mazegen-1.0.0-py3-none-any.whl`)

### Installing the Package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

```python
from mazegen import MazeGenerator

config = {
    "WIDTH": 15,
    "HEIGHT": 11,
    "ENTRY": (0, 0),
    "EXIT": (14, 10),
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": True,
}

gen = MazeGenerator(config)
gen.run()
```

### Accessing the Generated Structure

```python
maze = gen.maze          # Maze object
grid = maze.grid         # list[list[Cell]] — 2D grid of Cell objects
width = maze.width       # int
height = maze.height     # int

# Each Cell has:
cell = grid[y][x]
cell.walls    # int bitmask (N=1, E=2, S=4, W=8)
cell.cell42   # bool — part of "42" decorative pattern
cell.in_path  # bool — on the solution path
```

### Solving the Maze

```python
from mazegen import MazeSolver

solver = MazeSolver(gen.maze)
path = solver.solve(config["ENTRY"], config["EXIT"])
# path: list[tuple[int, int]] — list of (dx, dy) direction moves
```

### Custom Parameters

All configuration is passed via the `config` dictionary. Set `PERFECT=False` to generate imperfect mazes with loops. The `seed` is generated randomly internally but can be set by subclassing `MazeGenerator` and overriding `self.seed`.

### Building the Package from Source

```bash
pip install build
python -m build
# Produces dist/mazegen-*.whl and dist/mazegen-*.tar.gz
```

---

## Visual Representation

The terminal renderer draws the maze using ANSI escape codes and block characters. Each cell is rendered as a 5-character-wide column with wall segments using `▒` characters.

**Interactive menu options:**

| Key | Action |
|-----|--------|
| `1` | Re-generate a new maze |
| `2` | Show / Hide the shortest solution path |
| `3` | Rotate wall colors (random palette each toggle) |
| `4` | Quit |

**Visual elements:**
- Entry cell: blinking green `█`
- Exit cell: blinking red `█`
- Solution path: green `•` dots (when shown)
- "42" pattern cells: filled purple background
- Walls: customizable colored background blocks

---

## Team & Project Management

### Team Members

| Member | Role |
|--------|------|
| `lde-frei` | *maze generation, solving and rendering algorithm, initial project structure, docstrings* |
| `victode-` | *flake8, mypy, makefile, parser, documentation, structural organization and improvements* |

### Planning

*In the beginning, we already had all planned out about what algorithm we'd use and how the functions and classes would be. It was a little weird to organize it into isolated modules for better reusability. Trying to understand how the Cells, grid and binary logic worked was very tricky, but we feel everything worked just like expected.*

### What Could Be Improved

Adding a proper seed parameter to the config, supporting MLX rendering, multiple generation algorithms.

### Tools Used

- **Python 3.10+** — core language
- **flake8** — PEP 8 linting
- **mypy** — static type checking
- **AI assistance** — used to brainstorm algorithm structure and explore edge cases in the BFS solver; all generated code was reviewed, tested, and understood before integration.

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explained — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Python `collections.deque` — official docs](https://docs.python.org/3/library/collections.html#collections.deque)
- [ANSI escape codes reference](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)

**AI usage:** AI tools were used to assist with documentation drafting, exploring edge cases in the maze validation logic, and reviewing the BFS implementation. All output was critically reviewed and validated against the subject requirements and tested manually.
