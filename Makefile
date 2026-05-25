P3 = python3
VENV = venv
ACTIVATE = . $(VENV)/bin/activate

MAIN = a_maze_ing.py
CONFIG = config.txt

PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
RM = rm -rf

all: run

install:
	$(P3) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created successfully."

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	$(RM) $(VENV)

lint:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict

re: clean run

.PHONY: all install run debug clean lint lint-strict re