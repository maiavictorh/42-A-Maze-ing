P3=python3
VENV=venv

setup:
	$(P3) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	@echo "\n\33[32mVirtual Enviromenment created successfully!\33[0m"
	@echo " To activate the Enviromenment, execute:"
	@echo "    source $(VENV)/bin/activate"

install:
	$(VENV)/bin/pip install -r requirements.txt

run:
	$(VENV)/bin/$(P3) a_maze_ing.py config.txt

debug:

clean:
	rm -rf ./$(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:

.PHONY: setup install run debug clean lint lint-strict