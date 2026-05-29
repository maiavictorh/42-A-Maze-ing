P3 = python3
VENV = venv
PIP = $(VENV)/bin/pip
P3_VENV = $(VENV)/bin/python3
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
RM = rm -rf

MAIN = a_maze_ing.py
CONFIG = config.txt

all: run

install:
	$(P3) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created successfully."

run:
	$(P3_VENV) $(MAIN) $(CONFIG)

debug:
	$(P3_VENV) -m pdb $(MAIN) $(CONFIG)

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
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --strict

.PHONY: all install run debug clean lint lint-strict re