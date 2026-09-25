# Data Science Practice — developer commands
# Usage: make install | make test | make nb | make data | make clean

# Prefer the project virtualenv when it exists, else fall back to system python.
VENV_PY := $(wildcard .venv/bin/python)
PY := $(if $(VENV_PY),$(VENV_PY),python3)
PIP := .venv/bin/pip

.PHONY: help install test nb data clean

help:
	@echo "make install   create .venv and install pinned requirements"
	@echo "make test      run the offline-safe test suite"
	@echo "make nb        execute notebooks that need no network"
	@echo "make data      download every module dataset into data/raw"
	@echo "make clean     remove caches and generated databases"

install:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

test:
	$(PY) -m pytest -q tests

nb:
	$(PY) scripts/run_notebooks.py

data:
	$(PY) scripts/download_data.py --all

clean:
	rm -rf .pytest_cache
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} +
	rm -f data/processed/*.db
