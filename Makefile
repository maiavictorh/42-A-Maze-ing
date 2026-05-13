P3=python3
VENV=venv
CONFIG="config.txt"

setup:
	$(P3) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	@echo "\n\33[32mVirtual Environment created successfully!\33[0m"
	@echo " To activate the Environment, execute:"
	@echo "    source $(VENV)/bin/activate"

install:
	$(VENV)/bin/pip install -r requirements.txt

run:
	@test -d $(VENV) || (echo "\33[93;1mRun 'make setup' first\33[0m"; exit 1)
	$(VENV)/bin/$(P3) a_maze_ing.py $(CONFIG)

debug:
	$(VENV)/bin/$(P3) -m pdb a_maze_ing.py $(CONFIG)

clean:
	rm -rf ./$(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "\n\33[93mDon't forget to deactivate $(VENV)\33[0m"

lint:
	flake8 src/*.py utils/*.py a_maze_ing.py
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:

.PHONY: setup install run debug clean lint lint-strict